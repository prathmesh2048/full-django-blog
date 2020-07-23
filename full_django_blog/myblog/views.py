from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Post
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .forms import UserProfileForm, UserUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    template_name = 'myblog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


# @method_decorator(login_required, name='dispatch')
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    # context is automatically called 'object'


class PostCreateView(LoginRequiredMixin, CreateView):  # context rendered is 'form'
    model = Post
    fields = ['title', 'content']

    # success_url = reverse_lazy('detail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# This view does'nt requires a template


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ):   # context rendered is 'form' , this order is toooo important
    model = Post
    fields = ['title', 'content']
    # success_url = reverse_lazy('detail')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = '/'

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True
        else:
            raise Http404("You are not allowed to edit this Post")


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True
        else:
            raise Http404("You are not allowed to delete this Post")


@login_required
def profile(request):
    template = 'account/profile.html'
    details = Profile.objects.get(user=request.user)
    if request.method == "POST":
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'your profile has been updated !')
            return redirect('/profile')
    else:
        p_form = UserProfileForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {'details': details,
               'u_form': u_form,
               'p_form': p_form}
    return render(request, template, context)
