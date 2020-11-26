 
# Stock Rule

allow(actor, "retrieve", stock: food::Stock) if
    stock.owner = actor;

allow(actor, "retrieve", transfer: food::Transfer) if
    transfer.owner = actor;
