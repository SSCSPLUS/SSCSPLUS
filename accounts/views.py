from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from decimal import Decimal
from .models import Transaction, CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == 'active':
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'accounts/login.html', {'error': 'এই অ্যাকাউন্টটি সক্রিয় নয়। অনুগ্রহ করে অ্যাডমিনের সাথে যোগাযোগ করুন।'})
        else:
            return render(request, 'accounts/login.html', {'error': 'ভুল ইউজারনেম বা পিন'})
    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):
    txns = Transaction.objects.filter(user=request.user)
    total_credit = txns.filter(transaction_type='credit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_debit = txns.filter(transaction_type='debit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    balance = total_credit - total_debit
    mini_statement = txns.order_by('-date', '-created_at')[:5]
    pending_txns = txns.filter(transaction_type='debit', description__icontains='pending')

    return render(request, 'accounts/dashboard.html', {
        'balance': balance,
        'total_credit': total_credit,
        'total_debit': total_debit,
        'mini_statement': mini_statement,
        'pending_txns': pending_txns,
    })


@login_required
def statement_view(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    total_credit = txns.filter(transaction_type='credit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_debit = txns.filter(transaction_type='debit').aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(request, 'accounts/statement.html', {
        'transactions': txns,
        'total_credit': total_credit,
        'total_debit': total_debit,
        'balance': total_credit - total_debit,
    })


@login_required
def ft_view(request):
    return render(request, 'accounts/ft.html')


@login_required
def pin_change_view(request):
    if request.method == 'POST':
        old_pin = request.POST.get('old_pin')
        new_pin = request.POST.get('new_pin')
        confirm_pin = request.POST.get('confirm_pin')

        if not old_pin or not new_pin or not confirm_pin:
            return render(request, 'accounts/pin_change.html', {'error': 'সব ফিল্ড পূরণ করুন'})
        if not request.user.check_password(old_pin):
            return render(request, 'accounts/pin_change.html', {'error': 'পুরনো পিন ভুল হয়েছে'})
        if new_pin != confirm_pin:
            return render(request, 'accounts/pin_change.html', {'error': 'নতুন পিন এবং কনফার্ম পিন মিলে না'})
        if len(new_pin) < 4:
            return render(request, 'accounts/pin_change.html', {'error': 'পিন কমপক্ষে ৪ ডিজিটের হতে হবে'})

        request.user.set_password(new_pin)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, 'accounts/pin_change.html', {'success': 'পিন সফলভাবে পরিবর্তন করা হয়েছে'})

    return render(request, 'accounts/pin_change.html')


@login_required
def transfer_view(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient', '').strip()
        amount_str = request.POST.get('amount')
        pin = request.POST.get('pin')

        if not recipient_username or not amount_str or not pin:
            return render(request, 'accounts/transfer.html', {'error': 'সব ফিল্ড পূরণ করুন'})

        try:
            amount = Decimal(amount_str)
        except Exception:
            return render(request, 'accounts/transfer.html', {'error': 'অবৈধ পরিমাণ'})

        if amount <= 0:
            return render(request, 'accounts/transfer.html', {'error': 'পরিমাণ শূন্যের বেশি হতে হবে'})

        try:
            recipient = CustomUser.objects.get(username=recipient_username)
        except CustomUser.DoesNotExist:
            return render(request, 'accounts/transfer.html', {'error': 'ইউজার খুঁজে পাওয়া যায়নি'})

        if recipient == request.user:
            return render(request, 'accounts/transfer.html', {'error': 'নিজের কাছে ট্রান্সফার করা যাবে না'})

        txns = Transaction.objects.filter(user=request.user)
        total_credit = txns.filter(transaction_type='credit').aggregate(total=Sum('amount'))['total'] or 0
        total_debit = txns.filter(transaction_type='debit').aggregate(total=Sum('amount'))['total'] or 0
        balance = total_credit - total_debit

        if balance < amount:
            return render(request, 'accounts/transfer.html', {'error': 'পর্যাপ্ত ব্যালেন্স নেই'})

        if not request.user.check_password(pin):
            return render(request, 'accounts/transfer.html', {'error': 'পিন ভুল হয়েছে'})

        today = timezone.now().date()

        Transaction.objects.create(
            user=request.user,
            transaction_type='debit',
            amount=amount,
            description=f'Transfer to {recipient.username}',
            date=today,
            entered_by=request.user,
        )
        Transaction.objects.create(
            user=recipient,
            transaction_type='credit',
            amount=amount,
            description=f'Transfer from {request.user.username}',
            date=today,
            entered_by=request.user,
        )

        return render(request, 'accounts/transfer.html', {'success': f'{amount} টাকা {recipient.username} এ ট্রান্সফার করা হয়েছে'})

    return render(request, 'accounts/transfer.html')


@staff_member_required
def admin_stats_view(request):
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(status='active').count()
    total_txns = Transaction.objects.count()
    total_credit = Transaction.objects.filter(transaction_type='credit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_debit = Transaction.objects.filter(transaction_type='debit').aggregate(
        total=Sum('amount')
    )['total'] or 0
    balance = total_credit - total_debit
    recent_txns = Transaction.objects.select_related('user').order_by('-created_at')[:10]
    monthly_stats = (
        Transaction.objects
        .annotate(month=TruncMonth('date'))
        .values('month', 'transaction_type')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )[:12]
    user_balances = []
    for user in CustomUser.objects.all()[:10]:
        uc = Transaction.objects.filter(user=user, transaction_type='credit').aggregate(t=Sum('amount'))['t'] or 0
        ud = Transaction.objects.filter(user=user, transaction_type='debit').aggregate(t=Sum('amount'))['t'] or 0
        user_balances.append({'user': user, 'balance': uc - ud})

    return render(request, 'admin/sscs_stats.html', {
        'total_users': total_users,
        'active_users': active_users,
        'total_txns': total_txns,
        'total_credit': total_credit,
        'total_debit': total_debit,
        'balance': balance,
        'recent_txns': recent_txns,
        'monthly_stats': monthly_stats,
        'user_balances': user_balances,
        'title': 'Admin Dashboard',
    })


def logout_view(request):
    logout(request)
    return redirect('login')
