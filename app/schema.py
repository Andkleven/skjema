import graphene 
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import InputObjectType
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
import django_filters
from copy import deepcopy
import json, ast


from .models import CreateProject 




class CreateProjectNode(DjangoObjectType):
    class Meta:
        model = CreateProject
        fields = ('__all__')


class Query(graphene.ObjectType):
    create_project                      = graphene.List(CreateProjectNode,
                                                        id=graphene.Int())

    def resolve_create_project(root, info, id=False, **input):
        # login(info)
        qc = CreateProject.objects.all()
        if id:
            return qc.filter(id=id).order_by('id')
        return qc





def merge_data(old_data, new_data):
    old_data = old_data.get().data
    if 0 < len(old_data):
        old_data = json.loads(old_data)
    else:
        old_data = {}
    if 0 < len(new_data):
        new_data = json.loads(new_data)
    else:
        new_data = {}
    data = json.dumps({**old_data, **new_data})
    return data




class CreateProjectGraphql(graphene.Mutation):
    new = graphene.Field(CreateProjectNode)

    class Input:
        id                                          = graphene.Int()
        data                                        = graphene.String()

    def mutate(root, info, id=0, data='', **input):
        # login(info)   
        if id:
            create_project = CreateProject.objects.filter(pk=id).order_by('id')
            old_create_project = create_project.get().data
            if 2 < len(old_create_project): 
                old_number_of_categorys = json.loads(old_create_project)['numberOfCategorys']
                new_number_of_categorys = json.loads(data)['numberOfCategorys']
                if int(new_number_of_categorys) < int(old_number_of_categorys):
                    categorys = Category.objects.filter(create_project__id=id).order_by('id').order_by('id')
                    for i in range(int(old_number_of_categorys)-1, int(new_number_of_categorys)-1, -1):
                        try:
                            categorys[i].delete()
                        except:
                            pass
            data = merge_data(create_project, data)
            create_project.update(data=data, **input)
            return CreateProjectGraphql(new=create_project.get())

        else:
            create_project = CreateProject(data=data, **input)
            create_project.save()
            return CreateProjectGraphql(new=create_project)

        

class DeleteCreateProject(graphene.Mutation):
    deletet                                         = graphene.Boolean()

    class Input:
        id                                          = graphene.Int()

    def mutate(root, info, id=0, **input):
        # login(info)
        create_project = CreateProject.objects.filter(pk=id).order_by('id')
        if create_project.count() == 0:
            return DeleteCreateProject(deletet=False)
        create_project.delete()
        return DeleteCreateProject(deletet=True)

class Mutation(graphene.ObjectType):
    create_project                              = CreateProjectGraphql.Field()
    create_project_delete                       = DeleteCreateProject.Field()