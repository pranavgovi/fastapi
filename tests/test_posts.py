from myapp import schema
import pytest
def test_getallpost(authorized_client,test_posts):
    response=authorized_client.get("/posts")
    print(response.json())
    assert len(response.json())==len(test_posts)
    assert response.status_code==200

    for post in response.json():
        print(post)
        schema.Response(**post)


def test_unauthorized_client_getall(client,test_posts):
    response=client.get("/posts")
    assert response.status_code==401

def test_unauthorized_client_getone(client,test_posts):
    response=client.get("/posts")
    assert response.status_code==401

def test_authorized_client_getonerandom(authorized_client,test_posts,test_user):
    response=authorized_client.get("/posts/8888")
    assert response.status_code==404

def test_getonepost(authorized_client,test_posts,test_user):
    first_id=test_posts[0].blog_id
    
    response=authorized_client.get("/posts/{}".format(first_id))
    print(response.json())
    assert schema.Response(**response.json())
    assert response.status_code==200


@pytest.mark.parametrize("title,content,public",[
    ("tit1","content1",True),
    ("tit2","content2",False),
    ("tit3","content3",False)
])
def test_createpost(authorized_client,test_user,title,content,public):
    res=authorized_client.post("/posts",json={
        "title":title,"content":content,"public":public
    })
    assert res.status_code==201
    assert res.json()["title"]==title
    # assert res.json()["content"]==content
    assert res.json()["public"]==public
    assert schema.Response(**res.json())

def test_deletepost(authorized_client,test_user,test_posts):
    x=len(test_posts)
    res=authorized_client.delete("/posts/{}".format(test_posts[0].blog_id))
    print(res.json())
    assert res.status_code==200

def test_deletepost_notexist(authorized_client,test_user,test_posts):
    
    res=authorized_client.delete("/posts/99999")
    assert res.status_code==404

def test_delete_OtherUserPost_(authorized_client,test_user,test_posts):
 
    res=authorized_client.delete("/posts/{}".format(test_posts[1].blog_id))

    print(res.json())
    assert res.status_code==403

def test_updatepost(authorized_client,test_user,test_posts):
    updated_post={
        "title":"test1",
        "content":"test_content",
        "public":True
    }
    res=authorized_client.put("/posts/{}".format(test_posts[0].blog_id),json=updated_post)
    assert res.status_code==200
    assert res.json()["title"]==updated_post["title"]

def test_update_otherUserPost(authorized_client,test_user,test_posts):
    updated_post={
        "title":"testdddj1",
        "content":"test_cddjjdontent",
        "public":True
    }
    res=authorized_client.put("/posts/{}".format(test_posts[1].blog_id),json=updated_post)
    assert res.status_code==403