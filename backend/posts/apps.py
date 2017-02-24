from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Post'))    
