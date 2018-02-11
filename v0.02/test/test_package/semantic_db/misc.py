import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()

# put this here for now:
# http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
# 6/8/2014: Doh! There is a bug in sorting things like 0 vs 00 vs 000.
def natural_sorted(list, key=lambda s:s):
    """
    Sort the list into natural alphanumeric order.
    """
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)
#    list.sort(key=sort_key)
    return sorted(list,key=sort_key)

# convert float to int if possible:
def float_to_int(x,t=3):
  if float(x).is_integer():
    return str(int(x))
#  return str("%.3f" % x)
  return str(round(x,t))
  

# need to think on how we want |> and <| to behave.
# eg, currently <*||> returns 1. May want 0.
def labels_match(label_1,label_2):                                               # TODO. Is this even used anywhere anymore?? Can we delete it?
  logger.debug("label_1: " + label_1)
  logger.debug("label_2: " + label_2)

  truth_var = True

  one = label_1.lower()  # make label compare case insensitive
  two = label_2.lower()  # hrrmm... may not want this ....
  if one[0] == '!':   # for now only consider bra's with <!x| rather than kets |!x>
    one = one[1:]     # though it is not much work to extend it.
    truth_var = False

  logger.debug("one: " + one)
  logger.debug("two: " + two)
  if one == two:
    return truth_var
  a_cat = one.split(': ')
  b_cat = two.split(': ')
  if a_cat[-1] == '*':
    new_a_cat = a_cat[:-1]
    new_b_cat = b_cat[:len(new_a_cat)]
    if new_a_cat == new_b_cat:
      return truth_var
    else:
      return not truth_var
  if b_cat[-1] == '*':
    new_b_cat = b_cat[:-1]
    new_a_cat = a_cat[:len(new_b_cat)]
    if new_b_cat == new_a_cat:
      return truth_var
    else:
      return not truth_var
  return not truth_var

# Pretty sure it is correct.
def label_descent(x):                           # can we optimize this at all? Does it matter?
  logger.info("ket: " + x)
  result = [x]
  if x == "*":
    return result
  if x.endswith(": *"):
    x = x[:-3]
  while True:
    try:
      x,null = x.rsplit(": ",1)
      result.append(x + ": *")
    except:
      result.append("*")
      return result

def list2sp(one):
  r = superposition()
  if type(one) == list:
    for x in one:                                # what do we want to do if type(x) is not int, float or string?
      if type(x) == int or type(x) == float:
        r.add("number: " + str(x))
      elif type(x) == str:
        r.add(x)
  return r

