from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
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
