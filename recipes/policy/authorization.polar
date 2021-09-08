 
# Recipe Rules

allow(actor, "retrieve", recipe: recipes::Recipe) if
    recipe.owner = actor;

allow(actor, "retrieve", ingredient: recipes::Ingredient) if
    ingredient.owner = actor;

allow(actor, "retrieve", unit: recipes::Unit) if
    unit.owner = actor;

allow(actor, "retrieve", step: recipes::Step) if
    step.owner = actor;
