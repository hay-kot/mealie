import datetime
import json
from pathlib import Path
from typing import Any, List, Optional

from db.recipe_models import RecipeDocument
from pydantic import BaseModel, validator
from slugify import slugify

from services.image_services import delete_image

CWD = Path(__file__).parent
ALL_RECIPES = CWD.parent.joinpath("data", "all_recipes.json")
IMG_DIR = CWD.parent.joinpath("data", "img")


class RecipeNote(BaseModel):
    title: str
    text: str


class RecipeStep(BaseModel):
    text: str


class Recipe(BaseModel):
    # Standard Schema
    name: str
    description: Optional[str]
    image: Optional[Any]
    recipeYield: Optional[str]
    recipeIngredient: Optional[list]
    recipeInstructions: Optional[list]
    totalTime: Optional[Any]

    # Mealie Specific
    slug: Optional[str] = ""
    categories: Optional[List[str]]
    tags: Optional[List[str]]
    dateAdded: Optional[datetime.date]
    notes: Optional[List[RecipeNote]]
    rating: Optional[int]
    rating: Optional[int]
    orgURL: Optional[str]
    extras: Optional[dict]

    class Config:
        schema_extra = {
            "example": {
                "name": "Chicken and Rice With Leeks and Salsa Verde",
                "description": "This one-skillet dinner gets deep oniony flavor from lots of leeks cooked down to jammy tenderness.",
                "image": "chicken-and-rice-with-leeks-and-salsa-verde.jpg",
                "recipeYield": "4 Servings",
                "recipeIngredient": [
                    "1 1/2 lb. skinless, boneless chicken thighs (4-8 depending on size)",
                    "Kosher salt, freshly ground pepper",
                    "3 Tbsp. unsalted butter, divided",
                ],
                "recipeInstructions": [
                    {
                        "text": "Season chicken with salt and pepper.",
                    },
                ],
                "slug": "chicken-and-rice-with-leeks-and-salsa-verde",
                "tags": ["favorite", "yummy!"],
                "categories": ["Dinner", "Pasta"],
                "notes": [{"title": "Watch Out!", "text": "Prep the day before!"}],
                "orgURL": "https://www.bonappetit.com/recipe/chicken-and-rice-with-leeks-and-salsa-verde",
                "rating": 3,
                "extras": {
                    "message": "Don't forget to defrost the chicken!"
                }
            }
        }

    @validator("slug", always=True, pre=True)
    def validate_slug(slug: str, values):
        name: str = values["name"]
        calc_slug: str = slugify(name)

        if slug == calc_slug:
            return slug
        else:
            slug = calc_slug
            return slug

    @classmethod
    def _unpack_doc(cls, document):
        document = json.loads(document.to_json())
        del document["_id"]

        document["dateAdded"] = document["dateAdded"]["$date"]

        return cls(**document)

    @classmethod
    def get_by_slug(_cls, slug: str):
        """ Returns a recipe dictionary from the slug """

        document = RecipeDocument.objects.get(slug=slug)

        return Recipe._unpack_doc(document)

    def save_to_db(self) -> str:
        recipe_dict = self.dict()

        try:
            extension = Path(recipe_dict["image"]).suffix
            recipe_dict["image"] = recipe_dict.get("slug") + extension
        except:
            recipe_dict["image"] = "no image"

        try:
            total_time = recipe_dict.get("totalTime")
            recipe_dict["totalTime"] = str(total_time)
        except:
            pass

        recipeDoc = RecipeDocument(**recipe_dict)
        recipeDoc.save()

        return recipeDoc.slug

    @staticmethod
    def delete(recipe_slug: str) -> str:
        """ Removes the recipe from the database by slug """
        delete_image(recipe_slug)
        document = RecipeDocument.objects.get(slug=recipe_slug)

        if document:
            document.delete()
            return "Document Deleted"

    def update(self, recipe_slug: str):
        """ Updates the recipe from the database by slug"""
        document = RecipeDocument.objects.get(slug=recipe_slug)

        if document:
            document.update(set__name=self.name)
            document.update(set__description=self.description)
            document.update(set__image=self.image)
            document.update(set__recipeYield=self.recipeYield)
            document.update(set__recipeIngredient=self.recipeIngredient)
            document.update(set__recipeInstructions=self.recipeInstructions)
            document.update(set__totalTime=self.totalTime)

            document.update(set__categories=self.categories)
            document.update(set__tags=self.tags)
            document.update(set__notes=self.notes)
            document.update(set__orgURL=self.orgURL)
            document.update(set__rating=self.rating)
            document.update(set__extras=self.extras)
            document.save()


def read_requested_values(keys: list, max_results: int = 0) -> List[dict]:
    """
    Pass in a list of key values to be run against the database. If a match is found
    it is then added to a dictionary inside of a list. If a key does not exist the
    it will simply not be added to the return data.

    Parameters:
        keys: list

    Returns: returns a list of dicts containing recipe data

    """
    recipe_list = []
    for recipe in RecipeDocument.objects.order_by("dateAdded").limit(max_results):
        recipe_details = {}
        for key in keys:
            try:
                recipe_key = {key: recipe[key]}
            except:
                continue

            recipe_details.update(recipe_key)

        recipe_list.append(recipe_details)

    return recipe_list
