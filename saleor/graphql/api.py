import graphene
from graphene import relay
from graphene_django.debug import DjangoDebug

from .category.types import resolve_categories
from .product.types import (
    CategoryType, ProductAttributeType, resolve_attributes, resolve_category)


class Query(graphene.ObjectType):
    attributes = graphene.List(
        ProductAttributeType,
        category_pk=graphene.Argument(graphene.Int, required=True))
    category = graphene.Field(
        CategoryType,
        pk=graphene.Argument(graphene.Int, required=True))
    categories = graphene.List(
        CategoryType,
        parent=graphene.Argument(graphene.Int, required=False))
    node = relay.Node.Field()
    root = graphene.Field(lambda: Query)
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_category(self, info, **args):
        pk = args.get('pk')
        return resolve_category(pk, info)

    def resolve_categories(self, info, **args):
        parent = args.get('parent')
        return resolve_categories(parent, info)

    def resolve_attributes(self, info, **args):
        category_pk = args.get('category_pk')
        return resolve_attributes(category_pk)

    def resolve_root(self, info):
        # Re-expose the root query object. Workaround for the issue in Relay:
        # https://github.com/facebook/relay/issues/112
        return Query()


schema = graphene.Schema(Query)
