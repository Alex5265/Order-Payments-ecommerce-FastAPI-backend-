import pytest
from fastapi import status
from fastapi.exceptions import HTTPException
from app.repositories.categories import CategoryRepository
from app.services.categories import CategoryService

@pytest.mark.asyncio
async def test_health_check(client):
    """Простой тест для проверки работы клиента"""
    response = await client.get("/categories/")
    assert response.status_code == status.HTTP_200_OK



# ============= GET /categories/ =============
@pytest.mark.asyncio
async def test_read_all_categories_success(client, mocker):
    mock_categories = [
        {"id": 1, "name": "electronics", 'parent_id': None, "is_active": True},
        {"id": 2, "name": "books", 'parent_id': None, "is_active": True}
    ]
    mock_service = mocker.patch.object(CategoryRepository,
                        "get_all",
                        return_value=mock_categories)

    response = await client.get("/categories/?skip=5&limit=20")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert response.json() == mock_categories
    assert data[1]["name"] == "books"
    mock_service.assert_called_once_with(skip=5, limit=20)

@pytest.mark.asyncio
async def test_read_all_categories_empty(client, mocker):
    mock_categories = []
    mock_service = mocker.patch.object(CategoryRepository,
                                       'get_all',
                                       return_value=mock_categories
                                       )
    response = await client.get("/categories/")

    assert  response.status_code == status.HTTP_200_OK
    assert response.json() == []
    mock_service.assert_called_once()


# ============= GET /categories/{id} =============
@pytest.mark.asyncio
async def test_read_category_success(client, mocker):
    mock_categories = {"id": 5, "name": "smartphones", 'parent_id': 1, "is_active": True}
    mock_service = mocker.patch.object(CategoryRepository,
                                       'get_by_id',
                                       return_value=mock_categories)
    response = await client.get("/categories/5")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_categories
    mock_service.assert_called_once_with(category_id=5)

@pytest.mark.asyncio
async def test_read_category_not_found(client, mocker):
    mock_categories = None
    mock_service = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    response = await client.get("/categories/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_service.assert_called_once_with(category_id=999)

@pytest.mark.asyncio
async def test_read_category_not_found(client, mocker):
    response = await client.get("/categories/abc")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# ============= POST /categories/ =============
@pytest.mark.asyncio
async def test_create_category_success(client, mocker):
    new_category_data = {"name": "NewSubCategory", "parent_id": 2}
    created_category = {"id": 15, "name": "NewSubCategory", "parent_id": 2, "is_active": True}

    mock_service = mocker.patch.object(CategoryRepository,
                                       "create",
                                       return_value=created_category)

    mock_categories = {"id": 2, "name": "smartphones", 'parent_id': 0, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_existing_name = mocker.patch.object(CategoryRepository,
                                       "get_by_name",
                                       return_value=None)

    response = await client.post("/categories/", json=new_category_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_category

@pytest.mark.asyncio
async def test_create_category_short_name(client, mocker):
    new_category_data = {"name": "AA"}
    created_category = {"id": 15, "name": "NewSubCategory", "parent_id": 2, "is_active": True}

    mock_service = mocker.patch.object(CategoryRepository,
                                       "create",
                                       return_value=created_category)

    mock_categories = {"id": 2, "name": "smartphones", 'parent_id': 0, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_existing_name = mocker.patch.object(CategoryRepository,
                                       "get_by_name",
                                       return_value=None)

    response = await client.post("/categories/", json=new_category_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    print(response.json())

@pytest.mark.asyncio
async def test_create_category_not_parents(client, mocker):
    new_category_data = {"name": "NewSubCategory", "parent_id": 2}
    created_category = {"id": 15, "name": "NewSubCategory", "parent_id": 2, "is_active": True}

    mock_service = mocker.patch.object(CategoryRepository,
                                       "create",
                                       return_value=created_category)

    mock_categories = None
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_existing_name = mocker.patch.object(CategoryRepository,
                                       "get_by_name",
                                       return_value=None)

    response = await client.post("/categories/", json=new_category_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Parent category not found'}

@pytest.mark.asyncio
async def test_create_category_already_exists(client, mocker):
    new_category_data = {"name": "NewSubCategory", "parent_id": 2}
    created_category = {"id": 15, "name": "NewSubCategory", "parent_id": 2, "is_active": True}

    mock_service = mocker.patch.object(CategoryRepository,
                                       "create",
                                       return_value=created_category)

    mock_categories = {"id": 2, "name": "smartphones", 'parent_id': 0, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_existing_name = mocker.patch.object(CategoryRepository,
                                       "get_by_name",
                                       return_value={"id": 15, "name": "NewSubCategory", "parent_id": 2, "is_active": True})

    response = await client.post("/categories/", json=new_category_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Category with this name already exists'}


# ============= PUT /categories/{id} =============
@pytest.mark.asyncio
async def test_update_category_success(client, mocker):
    update_data = {"name": "Megabooks", "parent_id": 1}
    updated_category = {"id": 2, "name": "Megabooks", 'parent_id': 1, "is_active": True}

    mock_categories = {"id": 1, "name": "electronics", 'parent_id': None, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)

    mock_service = mocker.patch.object(CategoryRepository,
                                       "update",
                                       return_value=updated_category)

    response = await client.put("/categories/2", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_category

async def test_update_category_partial_data(client, mocker):
    update_data = {"parent_id": 1}
    updated_category = {"id": 2, "name": "books", 'parent_id': 1, "is_active": True}

    mock_categories = {"id": 1, "name": "electronics", 'parent_id': None, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)

    mock_service = mocker.patch.object(CategoryRepository,
                                       "update",
                                       return_value=updated_category)

    response = await client.put("/categories/2", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == updated_category

@pytest.mark.asyncio
async def test_update_category_not_found(client, mocker):
    update_data = {"name": "Megabooks", "parent_id": None}
    updated_category = {"id": 2, "name": "Megabooks", 'parent_id': 1, "is_active": True}

    mock_categories = None
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)

    mock_service = mocker.patch.object(CategoryRepository,
                                       "update",
                                       return_value=updated_category)

    response = await client.put("/categories/2", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Category not found'}




# ============= DELETE /categories/{id} =============
@pytest.mark.asyncio
async def test_delete_category_success(client, mocker):
    deleted_categories = {"id": 2, "name": "books", 'parent_id': None, "is_active": False}

    mock_categories = {"id": 2, "name": "books", 'parent_id': None, "is_active": True}
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_service = mocker.patch.object(CategoryRepository,
                        "delete",
                        return_value=deleted_categories)

    response = await client.delete("categories/2")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == deleted_categories
    mock_service.assert_called_once_with(2)

@pytest.mark.asyncio
async def test_delete_category_not_found(client, mocker):
    deleted_categories = {"id": 2, "name": "books", 'parent_id': None, "is_active": False}

    mock_categories = None
    mock_existing_parent = mocker.patch.object(CategoryRepository,
                                       "get_by_id",
                                       return_value=mock_categories)
    mock_service = mocker.patch.object(CategoryRepository,
                        "delete",
                        return_value=deleted_categories)

    response = await client.delete("categories/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Category not found'}