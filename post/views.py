from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from tagging.views import TaggedObjectList

from .models import Post, Category



class Main(ListView):
    model = Post
    template_name = 'post/index.html'


class PostList(ListView):
    model = Post
    paginate_by = 2
    template_name = 'post/post_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = Category.objects.filter(parent_category=None)
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'category_slug' in self.kwargs:
            try:
                category = Category.objects.get(slug=self.kwargs['category_slug'])
                queryset = queryset.filter(category=category)
            except:
                pass

        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form})


def postfilter(request, pk):
    queryset = Post.objects.all()

    # departure_key = request.GET.get('departure_key', None)
    # arrive_key = request.GET.get('arrive_key', None)
    # date_key = request.GET.get('date_key', None)
    #
    # departure_area_q = Q(departure_area__icontains=departure_key)
    # arrive_area_q = Q(arrive_area__icontains=arrive_key)
    # date_q = Q(departure_date__icontains=date_key)
    #
    # if queryset.exists():
    #     check_plan = queryset.filter(departure_area_q & arrive_area_q & date_q)
    #
    # return redirect(check_plan)

class PostUpdate(UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    fields = ['title', 'text', 'tag']
    # success_url = get_absolute_url


from django.urls import reverse_lazy

class PostDelete(DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    success_url = reverse_lazy('post:post_list')

from django.utils.text import slugify

class PostCreate(CreateView):
    model = Post
    fields = ['category', 'title', 'text', 'tag']
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        #작성자 매칭 form.instatnce.author_id = self.request.user.id
        #slugify
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)


class PostTaggedObjectList(TaggedObjectList):
    model = Post
    allow_empty = True
    template_name = 'post/post_list.html'


from django.views.generic import TemplateView

class TagList(TemplateView):

    template_name = 'post/tag_list.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['tags'] = Tag.objects.filter(parent_category=None)
    #     return context_data
