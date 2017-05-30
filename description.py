import random
desc_owner = ""
desc_item = ""

def np():
	t = random.randint(1, 10)
	if t % 2 == 0:
		return dp() + " " + adj2() + " " + pn()
	else:
		return pn()

def dp():
	choices = ["the", "a"]
	return random.choice(choices)

def adjp():
	t = random.randint(1, 10)
	if t % 2 == 0:
		return adj()
	else:
		return adj() + " " + adjp()

def adj():
	choices = ["delicious", "succulent", "tasty", "hearty", "beautiful", "awe-inspiring"]
	return random.choice(choices)

def adj2():
	choices = ["famous", "skilled", "talented"]
	return random.choice(choices)

def n():
	choices = ["pizza", "burger", "pasta", "sushi", "soup", "french fries", "goose eggs", "lobster tails"]
	return random.choice(choices)

def pn():
	return desc_owner

def vp():
	t = random.randint(1, 10)
	if t % 2 == 0:
		return tv() + " " + adjp() + " " + n()
	else:
		return iv()

def tv():
	choices = ["baked", "cooked", "crafted", "assembled", "forged"]
	return random.choice(choices)

def iv():
	choices = ["is the best", "is renowned", "is the worst", "is mediocre at best", "is decent"]
	return random.choice(choices)

def sentence():
	return np() + " " + vp();

def gen_description(owner, item):	
	global desc_owner
	desc_owner = owner
	global desc_item
	desc_item = item
	desc = sentence()
	desc = (desc[0].upper()) + desc[1:]
	return desc