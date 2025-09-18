from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from django.db.models import Q
from .models import Advertisement, Response, City, Category, Tag
from .forms import AdvertisementForm, ResponseForm, TagForm


class CategoryAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/category_ads.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Advertisement.objects.filter(category=self.category)

        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'price', '-price', 'views', '-views']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()

        return context


class TagAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/tag_ads.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        queryset = Advertisement.objects.filter(tags=self.tag)

        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'price', '-price', 'views', '-views']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()

        return context


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/home.html'
    context_object_name = 'advertisements'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        city_slug = self.request.GET.get('city')
        if city_slug:
            queryset = queryset.filter(city__slug=city_slug)

        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'price', '-price', 'views', '-views']:
            queryset = queryset.order_by(sort_by)

        return queryset.select_related('author', 'city', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()[:10]
        context['cities'] = City.objects.all()[:10]
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_city'] = self.request.GET.get('city', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['search_query'] = self.request.GET.get('q', '')

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()

        return context


class UserAdvertisementListView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'ads/user_advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        return Advertisement.objects.filter(author=self.request.user).order_by('-created_at')


class AdminAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'ads/admin_advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        queryset = Advertisement.objects.filter(author__username__iexact='admin')

        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'price', '-price', 'views', '-views']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')

        return queryset.select_related('author', 'city', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()

        return context


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'ads/advertisement_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        advertisement = get_object_or_404(
            Advertisement.objects.select_related('author', 'city', 'category').prefetch_related('tags'),
            slug=slug
        )
        advertisement.increment_views()
        return advertisement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        advertisement = self.get_object()
        similar_ads = Advertisement.objects.filter(
            Q(category=advertisement.category) |
            Q(tags__in=advertisement.tags.all())
        ).exclude(id=advertisement.id).distinct()[:4]
        context['similar_ads'] = similar_ads
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
    model = Response
    form_class = ResponseForm
    template_name = 'ads/response_form.html'

    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, slug=self.kwargs['slug'])
        form.instance.sender = self.request.user
        form.instance.recipient = advertisement.author
        form.instance.advertisement = advertisement
        messages.success(self.request, 'Ваш отклик отправлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'slug': self.kwargs['slug']})


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


# ✅ Профиль пользователя
class ProfileView(DetailView):
    model = User
    template_name = 'ads/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['advertisements'] = Advertisement.objects.filter(author=user)
        context['received_responses'] = Response.objects.filter(recipient=user).select_related('advertisement', 'sender')
        context['sent_responses'] = Response.objects.filter(sender=user).select_related('advertisement', 'recipient')
        return context




