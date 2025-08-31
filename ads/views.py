from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import Advertisement, Response, City, Category, Tag
from .forms import AdvertisementForm, ResponseForm, TagForm

class CategoryAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/category_ads.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Advertisement.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TagAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/tag_ads.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Advertisement.objects.filter(tags=self.tag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'ads/add_tag.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'Тег успешно создан!')
        return super().form_valid(form)

class TagListView(ListView):
    model = Tag
    template_name = 'ads/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 20

class CityListView(ListView):
    model = City
    template_name = 'ads/city_list.html'
    context_object_name = 'cities'
    paginate_by = 50
    ordering = ['name']

class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/home.html'
    context_object_name = 'advertisements'
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()[:10]
        context['cities'] = City.objects.all()[:10]
        return context

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

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Advertisement, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context

class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'ads/advertisement_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)

class AdvertisementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'ads/advertisement_form.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Advertisement, slug=slug)

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Объявление успешно обновлено!')
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user == advertisement.author

class AdvertisementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Advertisement
    template_name = 'ads/advertisement_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Advertisement, slug=slug)

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user == advertisement.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Объявление успешно удалено!')
        return super().delete(request, *args, **kwargs)

class ResponseDetailView(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'ads/response_detail.html'

    def get_queryset(self):
        return Response.objects.filter(
            models.Q(sender=self.request.user) |
            models.Q(recipient=self.request.user)
        )

class ResponseCreateView(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    template_name = 'ads/response_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.advertisement = get_object_or_404(Advertisement, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = form.save(commit=False)
        response.advertisement = self.advertisement
        response.sender = self.request.user
        response.recipient = self.advertisement.author
        response.save()
        messages.success(self.request, 'Ваш отклик успешно отправлен!')
        return redirect('advertisement_detail', slug=self.advertisement.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisement'] = self.advertisement
        return context

class ResponseAcceptView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        return self.request.user == response.recipient

    def get(self, request, *args, **kwargs):
        response = get_object_or_404(Response, pk=kwargs['pk'])
        response.status = 'accepted'
        response.save()
        messages.success(request, 'Отклик принят!')
        return redirect('profile', username=request.user.username)

class ResponseRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        return self.request.user == response.recipient

    def get(self, request, *args, **kwargs):
        response = get_object_or_404(Response, pk=kwargs['pk'])
        response.status = 'rejected'
        response.save()
        messages.success(request, 'Отклик отклонён.')
        return redirect('profile', username=request.user.username)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'ads/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['advertisements'] = Advertisement.objects.filter(author=user)
        context['received_responses'] = Response.objects.filter(recipient=user).order_by('-created_at')
        context['sent_responses'] = Response.objects.filter(sender=user).order_by('-created_at')
        return context

