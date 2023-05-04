# README后端

### 1.day06 发布

##### 后端

- GET 获取临时COS密钥（临时密钥需要有上传和删除的权限）（APIView）
- GET 获取话题接口

  - url

    ```
    url(r'^topic/$', topic.TopicView.as_view()),
    ```

  - 序列化

    ```python
    class TopicSerializer(ModelSerializer):
        class Meta:
            model = models.Topic
            fields = "__all__"
    ```

  - view（读取所有的话题） 

    - APIView
    - ListAPIView（推荐，**ListAPIView默认有一个get方法来获取数据库中的所有数据并序列化返回，所以一般涉及到数据库的操作用ListAPIVIew**）

    ```python
    class TopicView(ListAPIView):
        serializer_class = TopicSerializer
        queryset = models.Topic.objects.all().order_by('-count')
    ```

- POST 提交 新闻信息

  - url

    ```
    url(r'^news/$', news.NewsView.as_view()),
    ```

  - 序列化

    ```python
    class CreateNewsTopicModelSerializer(serializers.Serializer):
        key = serializers.CharField()
        cos_path = serializers.CharField()
    
    
    class CreateNewsModelSerializer(serializers.ModelSerializer):
        imageList = CreateNewsTopicModelSerializer(many=True)
    
        class Meta:
            model = models.News
            exclude = ['user', 'viewer_count', 'comment_count']
    
        def create(self, validated_data):
            image_list = validated_data.pop('imageList')
            news_object = models.News.objects.create(**validated_data)
            data_list = models.NewsDetail.objects.bulk_create(
                [models.NewsDetail(**info, news=news_object) for info in image_list]
            )
            news_object.imageList = data_list
    
            if news_object.topic:
                news_object.topic.count += 1
                news_object.save()
    
            return news_object
    ```

    

  - view（读取所有的话题） 

    - APIView
    - CreateAPIView（推荐，**默认内置有一个post方法**）

    ```python
    class NewsView(CreateAPIView):
    	serializer_class = CreateNewsModelSerializer
        
        def perform_create(self, serializer):
            new_object = serializer.save(user_id=1)
            return new_object
    ```

### 2.API请求

`http://localhost/api/comment/?root=12`

api/urls.py中

`url(r'^comment/$',news.CommentView.as_view())` 

news.py中

```python
class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentRecord
        fields = "__all__"
        
class CommentView(APIView):
    def get(self,request,*args,**kwargs):
        root_id = request.query_params.get('root')
        # 1.获取这个根评论的所有子评论
        node_queryset = models.CommentRecord.objects.filter(root_id=root_id).order_by('id')
        # 2.序列化
        ser = CommentModelSerializer(instance=node_queryset,many=True)
        return Response(ser.data,status=200)
```

