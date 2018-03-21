----------------------------------------
|context> => |context: early US Presidents>

supported-ops |early US Presidents: _list> => |op: >
 |early US Presidents: _list> => |Washington> + |Adams> + |Jefferson> + |Madison> + |Monroe> + |Q Adams>

supported-ops |Washington> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Washington> => |number: 1>
president-era |Washington> => |year: 1789> + |year: 1790> + |year: 1791> + |year: 1792> + |year: 1793> + |year: 1794> + |year: 1795> + |year: 1796> + |year: 1797>
party |Washington> => |party: Independent>
full-name |Washington> => |person: George Washington>

supported-ops |person: George Washington> => |op: >
 |person: George Washington> => |US President: George Washington>

supported-ops |Adams> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Adams> => |number: 2>
president-era |Adams> => |year: 1797> + |year: 1798> + |year: 1799> + |year: 1800> + |year: 1801>
party |Adams> => |party: Federalist>
full-name |Adams> => |person: John Adams>

supported-ops |person: John Adams> => |op: >
 |person: John Adams> => |US President: John Adams>

supported-ops |Jefferson> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Jefferson> => |number: 3>
president-era |Jefferson> => |year: 1801> + |year: 1802> + |year: 1803> + |year: 1804> + |year: 1805> + |year: 1806> + |year: 1807> + |year: 1808> + |year: 1809>
party |Jefferson> => |party: Democratic-Republican>
full-name |Jefferson> => |person: Thomas Jefferson>

supported-ops |person: Thomas Jefferson> => |op: >
 |person: Thomas Jefferson> => |US President: Thomas Jefferson>

supported-ops |Madison> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Madison> => |number: 4>
president-era |Madison> => |year: 1809> + |year: 1810> + |year: 1811> + |year: 1812> + |year: 1813> + |year: 1814> + |year: 1815> + |year: 1816> + |year: 1817>
party |Madison> => |party: Democratic-Republican>
full-name |Madison> => |person: James Madison>

supported-ops |person: James Madison> => |op: >
 |person: James Madison> => |US President: James Madison>

supported-ops |Monroe> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Monroe> => |number: 5>
president-era |Monroe> => |year: 1817> + |year: 1818> + |year: 1819> + |year: 1820> + |year: 1821> + |year: 1822> + |year: 1823> + |year: 1824> + |year: 1825>
party |Monroe> => |party: Democratic-Republican>
full-name |Monroe> => |person: James Monroe>

supported-ops |person: James Monroe> => |op: >
 |person: James Monroe> => |US President: James Monroe>

supported-ops |Q Adams> => |op: president-number> + |op: president-era> + |op: party> + |op: full-name>
president-number |Q Adams> => |number: 6>
president-era |Q Adams> => |year: 1825> + |year: 1826> + |year: 1827> + |year: 1828> + |year: 1829>
party |Q Adams> => |party: Democratic-Republican>
full-name |Q Adams> => |person: John Quincy Adams>

supported-ops |person: John Quincy Adams> => |op: >
 |person: John Quincy Adams> => |US President: John Quincy Adams>

supported-ops |party: Democratic-Republican> => |op: founded> + |op: dissolved>
founded |party: Democratic-Republican> => |year: 1791>
dissolved |party: Democratic-Republican> => |year: 1825>
----------------------------------------
