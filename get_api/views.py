from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from blogpost.models import BlogPost
from myapi.serializers import BlogPostSerializer

class BlogPostApiView(View):
    def get(self, request, *args, **kwargs):
        # ۱. دریافت تمام آبجکت‌ها
        posts = BlogPost.objects.all()
        
        # ۲. مقداردهی صفحه‌بندی (مثلا 5 پست در هر صفحه)
        paginator = Paginator(posts, 5)
        
        # ۳. دریافت شماره صفحه از کوئری پارامتر
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        # ۴. سریالایز کردن داده‌های همین صفحه
        serializer = BlogPostSerializer(page_obj, many=True)
     #    response_data = serializer.data
        # ۵. ساخت ساختار پاسخ نهایی
        response_data = {
            "count": paginator.count,            # تعداد کل پست‌ها
            "total_pages": paginator.num_pages,  # تعداد کل صفحات
            "current_page": page_obj.number,     # شماره صفحه فعلی
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "results": serializer.data
        }
        
        return JsonResponse(response_data)

class PostDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        # ۱. دریافت تمام آبجکت‌ها
        post = get_object_or_404(BlogPost, pk=pk)
               
        serializer = BlogPostSerializer(post)
        # ۵. ساخت ساختار پاسخ نهایی
        return JsonResponse(serializer.data)