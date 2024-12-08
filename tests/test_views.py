"""
This is test functions with pytest for application
"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ecogiveapp.models import Item

##Test for register View
@pytest.mark.django_db
def test_register_valid_data(client):
    """
    This is test function with pytest for valid registration
    """
    response = client.post(reverse('register'), {
        'username': 'testuser1',
        'password': 'P@ssw0rd123',
        'confirm_password': 'P@ssw0rd123',
        'email': 'testuser1@gmail.com'
    })
    assert response.status_code == 302
    assert User.objects.filter(username='testuser1').exists()


@pytest.mark.django_db
def test_register_invalid_data(client):
    """
    This is test function with pytest for invalid registration
    """
    response = client.post(reverse('register'), {
        'username': 'testuser2',
        'password': 'P@ssw0rd123',
        'confirm_password': 'wrongpassword',
        'email': 'testuser2@example.com'
    })
    assert response.status_code == 200
    assert not User.objects.filter(username='testuser').exists()

##Test for user_login View
@pytest.mark.django_db
def test_user_login_valid(client):
    """
    This is test function with pytest for valid login
    """
    User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    response = client.post(reverse('login'), {
        'username': 'testuser1',
        'password': 'P@ssw0rd123'
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_login_invalid(client):
    """
    This is test function with pytest for invalid login
    """
    response = client.post(reverse('login'), {
        'username': 'testuser1',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200

#Test for user_logout View
@pytest.mark.django_db
def test_user_logout(client):
    """
    This is test function with pytest for user logout view
    """
    User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    client.login(username='testuser1', password='P@ssw0rd123')
    response = client.post(reverse('logout'))
    assert response.status_code == 302

##Test for add_item View
@pytest.mark.django_db
def test_add_item_valid(client):
    """
    This is test function with pytest for add item view
    """
    User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    client.login(username='testuser1', password='P@ssw0rd123')
    mock_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    response = client.post(reverse('add_item'), {
        'title': 'Test Item',
        'description': 'This is a test item.',
        'quantity': 1,
        'image': mock_image,
    })
    assert response.status_code == 302
    assert Item.objects.filter(title='Test Item').exists()


##Test for edit_item View
@pytest.mark.django_db
def test_edit_item(client):
    """
    This is test function with pytest for edit item view
    """
    user = User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    item = Item.objects.create(
        title='Old Item', description='Old description', quantity=1, owner=user)
    client.login(username='testuser1', password='P@ssw0rd123')
    response = client.post(reverse('edit_item', args=[item.id]), {
        'title': 'Updated Item',
        'description': 'Updated description',
        'quantity': 2
    })
    assert response.status_code == 302
    item.refresh_from_db()
    assert item.title == 'Updated Item'
    assert item.quantity == 2

##Test for delete_item View
@pytest.mark.django_db
def test_delete_item(client):
    """
    This is test function with pytest for delete item view
    """
    user = User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    item = Item.objects.create(
        title='Test Item', description='Test Description', quantity=1, owner=user)
    client.login(username='testuser1', password='P@ssw0rd123')
    response = client.post(reverse('delete_item', args=[item.id]))
    assert response.status_code == 302
    assert not Item.objects.filter(id=item.id).exists()

##Test for inquire_item View
@pytest.mark.django_db
def test_inquire_item(client):
    """
    This is test function with pytest for user inquire item view
    """
    user = User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    item = Item.objects.create(
        title='Test Item', description='Test Description', quantity=1, owner=user)
    response = client.post(reverse('inquire_item', args=[item.id]), {
        'email': 'user@example.com',
        'message': 'I am interested in your item.'
    })
    assert response.status_code == 302


##Test for dashboard View
@pytest.mark.django_db
def test_dashboard_view(client):
    """
    This is test function with pytest for user dashboard view
    """
    User.objects.create_user(username='testuser1', password='P@ssw0rd123')
    client.login(username='testuser1', password='P@ssw0rd123')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert 'items' in response.context
