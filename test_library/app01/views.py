from django.shortcuts import render,HttpResponse,redirect,reverse
from app01 import models
# Create your views here.

def publisher_list(request):
    all_publisher = models.Publisher.objects.all()
    for i in all_publisher:
        print(i)
    return render(request,"publisher_list.html",{"all_publisher":all_publisher})


def publisher_add(request):
    error = ""
    if request.method == "GET":
        return render(request,"publisher_add.html")
    else:
        pub_name = request.POST.get("name")
        pub_addr = request.POST.get("addr")
        if not pub_name:
            error = "出版社不能为空"
        elif models.Publisher.objects.filter(name=pub_name):
            error = "出版社重复"
        else:
            ret = models.Publisher.objects.create(name=pub_name,addr=pub_addr)
            return redirect('/publisher_list/')
    return render(request,"publisher_add.html",{"error":error})

def publisher_del(request):
    id = request.GET.get('id')
    ret = models.Publisher.objects.filter(pid=id)
    if not ret:
        return HttpResponse("数据不存在")
    ret.delete()
    return redirect('/publisher_list/')


def publisher_edit(request):
    error = ''
    pid = request.GET.get('id')
    pub = models.Publisher.objects.filter(pid=pid)
    if not pub:
        error = "出版社不存在"
    pub_obj = pub[0]
    if request.method == "POST":
        pub_name = request.POST.get("pub_name")
        pub_addr = request.POST.get("pub_addr")
        if not pub_name:
            error = "出版社不能为空"
        elif models.Publisher.objects.filter(name=pub_name):
            error = "出版社名字重复"
        elif pub_obj.name == pub_name and pub_obj.addr == pub_addr:
            error = "数据未修改"
        else:
            pub_obj.name = pub_name
            pub_obj.addr = pub_addr
            pub_obj.save()
            return redirect('/publisher_list/')

    return render(request,"publisher_edit.html",{"error":error})

def book_list(request):
    all_books = models.Book.objects.all()
    return render(request,'book_list.html',{"all_books":all_books})

def book_add(request):
    if request.method == "POST":
        # 获取数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # 将数据插入到数据库
        # models.Book.objects.create(title=book_name,pub=models.Publisher.objects.get(pk=pub_id))
        models.Book.objects.create(title=book_name,pub_id=pub_id)
        # 跳转到书籍的展示页面
        return redirect(reverse('book'))

    # 查询所有的出版社
    all_publishers = models.Publisher.objects.all()
    return render(request,'book_add.html',{"all_publishers":all_publishers})

def book_del(request):
    # 获取要删除的对象删除
    pk = request.GET.get('id')
    models.Book.objects.filter(pk=pk).delete()
    # 跳转到展示页面
    return redirect(reverse('book'))

# 编辑书籍
def book_edit(request):
    # 获取要编辑的书籍对象
    pk = request.GET.get('id')
    book_obj = models.Book.objects.get(pk=pk)

    if request.method == 'POST':
        # 获取提交的数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # 修改数据
        book_obj.title = book_name
        # book_obj.pub_id = pub_id  #直接在本表改，而不用查询
        book_obj.pub = models.Publisher.objects.get(pid=pub_id)
        book_obj.save()

        return redirect(reverse('book'))

    # 查询所有的出版社
    all_publishers = models.Publisher.objects.filter()
    return render(request,'book_edit.html',{"all_publishers":all_publishers})

# 展示作者
def author_list(request):
    # 查询所有的作者
    all_authors = models.Author.objects.all()
    # for i in all_authors:
    #     print(i,type(i))
    #     print(i.pk,type(i.pk))
    #     print(i.name,type(i.name))
    #     print(i.books,type(i.books)) #关系管理对象
    #     print(i.books.all(),type(i.books.all()))
    return render(request,'author_list.html',{"all_authors":all_authors})

# 增加作者
def author_add(request):

    if request.method == 'POST':
        # 获取post请求提交数据
        author_name = request.POST.get('author_name')
        books = request.POST.getlist('books')
        # 存入数据
        author_obj = models.Author.objects.create(name=author_name)
        author_obj.books.set(books)
        # 跳转到展示页面
        return redirect('/app01/author_list/')
    # 查询所有的书籍
    all_books = models.Book.objects.all()
    return render(request,'author_add.html',{"all_books":all_books})

# 删除作者
def author_del(request):
    # 获取要删除对象的id
    pk = request.GET.get('pk')
    # 获取要删除的对象 删除
    models.Author.objects.filter(pk=pk).delete()
    # 跳转到展示页面
    return redirect(reverse("author"))

# 编辑作者
def author_edit(request):
    # 查询编辑的作者对象
    pk = request.GET.get('pk')
    # author_obj = models.Author.objects.filter(pk=pk) # 因为filter查出来是一个queryset对象，当作字典用的话就按字典取值即可
    # author_obj = author_obj[0]
    author_obj = models.Author.objects.get(pk=pk)  #如果是编辑的话，直接用get，正常程序需要做个try，做个异常处理
    if request.method == "POST":
        # 获取提交的数据
        author_name = request.POST.get("author_name")
        books = request.POST.getlist("books")
        # 修改对象的数据
        author_obj.name = author_name
        author_obj.save()
        # 多对多的关系
        author_obj.set(books) #  每次重新设置
        # 重定向
        return redirect('/author_list/')

    # 查询所有的书籍
    all_books = models.Book.objects.all()
    return render(request,'author_edit.html',{"author_obj":author_obj,"all_books":all_books})