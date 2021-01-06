 
allow(actor, "retrieve", authdetails: userauth::AuthDetails) if
    authdetails.user = actor;

allow(actor, "retrieve", homegroup: userauth::HomeGroup) if
    homegroup.userprofiles.user = actor;
