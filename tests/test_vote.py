from myapp import schema,models
import pytest


@pytest.fixture()
def test_automaticvote(authorized_client,test_posts,session,test_user):
    vote=models.Voting(post_id=test_posts[0].blog_id,user_id=test_user['id'])
    session.add(vote)
    session.commit()

    


def test_alreadyLiked(authorized_client,test_posts,test_automaticvote):
    vote_data={
        "post_id":1,
        "dir":True
    }
    res=authorized_client.post("/vote",json=vote_data)
    print(res.json())
    assert res.status_code==409
  
def test_firstLike(authorized_client,test_posts):
    vote_data={
        "post_id":1,
        "dir":True
    }
    res=authorized_client.post("/vote",json=vote_data)
    print(res.json())
    assert res.status_code==200

def test_deleteAlreadyLikedVote(authorized_client,test_posts,test_automaticvote):
    vote_data={
        "post_id":1,
        "dir":False
    }
    res=authorized_client.post("/vote",json=vote_data)
    print(res.json())
    assert res.status_code==200


def test_VoteOnNonexistingPost(authorized_client,test_posts):
    vote_data={
        "post_id":1010101,
        "dir":True
    }
    res=authorized_client.post("/vote",json=vote_data)
    print(res.json())
    assert res.status_code==404

#when unauthorised client tries to vote
def test_VotebyUnauthorised(client,test_posts):
    vote_data={
        "post_id":test_posts[0].blog_id,
        "dir":True
    }
    res=client.post("/vote",json=vote_data)
    print(res.json())
    assert res.status_code==401