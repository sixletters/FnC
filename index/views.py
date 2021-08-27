from django.shortcuts import render

# Create your views here.

# short cut that allows to retrieve objecct, raises a 404 exception if object does not exist
from django.shortcuts import get_object_or_404

# Permission Denied reaise an HTTP 403 exception when called
from django.core.exceptions import PermissionDenied

# generic views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Assert users to have the right permissions when accessing a view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# Photo model
from .models import Photo


class PhotoListView(ListView):
    model = Photo
    template_name = 'index/list.html'
    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'index/taglist.html'

    def get_tag(self):
        return self.kwargs.get('tag')

    # by default will return self.model.objects.all()
    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'index/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['title', 'description', 'image', 'tags']
    template_name = 'index/create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user

        return super().form_valid(form)


class UserIsSubmitter(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'index/update.html'
    model = Photo
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'index/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')
