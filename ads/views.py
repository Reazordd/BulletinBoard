from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from .models import Advertisement, Response, City
from .forms import AdvertisementForm, ResponseForm

class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/home.html'
    context_object_name = 'advertisements'
    ordering = ['-created_at']
    paginate_by = 10

class UserAdvertisementListView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'ads/user_advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        return Advertisement.objects.filter(author=self.request.user).order_by('-created_at')

class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'ads/advertisement_detail.html'

class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AdvertisementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user == advertisement.author

class AdvertisementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Advertisement
    success_url = reverse_lazy('home')

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user == advertisement.author

class ResponseDetailView(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'ads/response_detail.html'

    def get_queryset(self):
        return Response.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(recipient=self.request.user)
        )

@login_required
def create_response(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.sender = request.user
            response.recipient = advertisement.author
            response.save()
            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('advertisement_detail', pk=pk)
    else:
        form = ResponseForm()
    return render(request, 'ads/response_form.html', {'form': form, 'advertisement': advertisement})

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if request.user != response.recipient:
        return redirect('home')
    response.status = 'accepted'
    response.save()
    messages.success(request, 'Отклик принят!')
    return redirect('profile', username=request.user.username)

@login_required
def reject_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if request.user != response.recipient:
        return redirect('home')
    response.status = 'rejected'
    response.save()
    messages.success(request, 'Отклик отклонён.')
    return redirect('profile', username=request.user.username)

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    advertisements = Advertisement.objects.filter(author=user)
    received_responses = Response.objects.filter(recipient=user).order_by('-created_at')
    sent_responses = Response.objects.filter(sender=user).order_by('-created_at')

    context = {
        'profile_user': user,
        'advertisements': advertisements,
        'received_responses': received_responses,
        'sent_responses': sent_responses,
    }

    return render(request, 'ads/profile.html', context)

