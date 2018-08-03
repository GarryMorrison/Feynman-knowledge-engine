
----------------------------------------
supported-ops |context> => |op: > + |op: previous>
 |context> => |context: friends>
previous |context> => |context: global context>

supported-ops |Fred> => |op: friends>
friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>

supported-ops |Sam> => |op: friends>
friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>

supported-ops |Jack> => |op: inverse-friends>
inverse-friends |Jack> => |Fred> + |Sam>

supported-ops |Harry> => |op: inverse-friends>
inverse-friends |Harry> => |Fred>

supported-ops |Ed> => |op: inverse-friends>
inverse-friends |Ed> => |Fred>

supported-ops |Mary> => |op: inverse-friends>
inverse-friends |Mary> => |Fred>

supported-ops |Rob> => |op: inverse-friends>
inverse-friends |Rob> => |Fred>

supported-ops |Patrick> => |op: inverse-friends>
inverse-friends |Patrick> => |Fred>

supported-ops |Emma> => |op: inverse-friends>
inverse-friends |Emma> => |Fred> + |Sam>

supported-ops |Charlie> => |op: inverse-friends>
inverse-friends |Charlie> => |Fred> + |Sam>

supported-ops |George> => |op: inverse-friends>
inverse-friends |George> => |Sam>

supported-ops |Rober> => |op: inverse-friends>
inverse-friends |Rober> => |Sam>

supported-ops |Frank> => |op: inverse-friends>
inverse-friends |Frank> => |Sam>

supported-ops |Julie> => |op: inverse-friends>
inverse-friends |Julie> => |Sam>
----------------------------------------
