import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 设置django环境，否则无法使用django的ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datacenter_drf.settings")
django.setup()

# 导入模型
from apps.feature.models import Feature

from apps.article.models import Chapter, Article

# 导入功能数据
# from DB_tools.data_features import features
from DB_tools.data_features_en import features

# 导入章节数据
from DB_tools.data_chapters import chapters

# 导入用户数据
from apps.user.models import UserProfile

# 导入文章数据
# from DB_tools.data_articles import articles
from DB_tools.data_articles_en import articles


# 导入功能数据
def import_feature():
    for feature in features:
        Feature.objects.create(
            title=feature["title"],
            percentage=feature["percentage"],
            content=feature["content"],
        )


def import_chapter():
    for chapter in chapters:
        Chapter.objects.create(
            content=chapter["content"],
            timestamp=chapter["timestamp"],
        )


def import_article():
    for article in articles:
        Article.objects.create(
            author=UserProfile.objects.get(id=article["author"]),
            ranking=article["ranking"],
            title=article["title"],
            content=article["content"],
            desc=article["desc"],
        )


if __name__ == "__main__":
    import_feature()
    import_chapter()
    import_article()
    print("data导入成功")
