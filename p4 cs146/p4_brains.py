
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'active'
    self.target = None
    self.have_resource = False



  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.
      #print("im idle!")
      if message == 'timer':
        if self.state == 'a':
          target = self.body.find_nearest("Mantis")
          self.body.follow(target)
          self.body.set_alarm(1)
        if self.have_resource == True and self.state == 'h':
          target = self.body.find_nearest("Nest")
          self.body.go_to(target)
          self.body.set_alarm(1)
        if self.have_resource == False and self.state == 'h':
          target = self.body.find_nearest("Resource")
          self.body.go_to(target)
          self.body.set_alarm(1)

      #move to functionality
      if message == 'order' and type (details) == tuple:
       print("i should be moving")
       x,y = details
       self.body.go_to((x,y))

      #idle functionality, stops the slug in its tracks. 
      if message == 'order' and details == 'i':
        self.state = 'i'
        print("im now idle")
        self.body.stop()
        self.body.state = 'idle'

      #build functionality
      if message == 'order' and details == 'b':
        self.state = 'b'
        print("build")
        #find nearest nest and approach it
        target = self.body.find_nearest("Nest")
        self.body.go_to(target)
        #self.body.set_alarm(10)

     #checking to see if the slug is hitting the nest
      if message == 'collide' and details['what'] == 'Nest':
        print("im feeding")
        nest = details['who']
        nest.amount += 0.01
        self.have_resource = False

      #start harvest mode
      if message == 'order' and details == 'h':
        print("h")
        self.state = 'h'
        if self.have_resource == True:
          print("i have a resource")
          target = self.body.find_nearest("Nest")
          self.body.go_to(target)
        elif self.have_resource == False:
          print("I dont have a resource")
          target = self.body.find_nearest("Resource")
          self.body.go_to(target)

      #attacking
      if message == 'order' and details == 'a':
        self.state = 'a'
        target = self.body.find_nearest("Mantis")
        self.body.follow(target)
        self.body.set_alarm(1)


      if message == 'collide' and details['what'] == 'Mantis':
        if self.state == 'a':
         mantis = details['who']
         mantis.amount -= 0.05


      #checking to see if slug is hitting the resource
      if message == 'collide' and details['what'] == 'Resource':
         if self.have_resource == False:
            resource = details['who']
            resource.amount -= 0.25
            self.have_resource = True
            self.body.set_alarm(1)
         if self.have_resource == True:
            self.have_resource = True
            self.body.set_alarm(1)
    #  if details['what'] == 'Slug':
      print(self.body.amount)

      #print(self.body.amount)
      #flee
      if self.body.amount < .5:
        print("FUCK IM GETTING KILLED")
        self.state = 'flee'
        target = self.body.find_nearest("Nest")
        self.body.go_to(target)
      if message == 'collide' and details['what'] == 'Nest':
        if self.state == 'flee':
          self.body.amount = 1
          self.state = 'a'
          self.body.set_alarm(1)

         #self.body.set_alarm(1)





world_specification = {
  'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 5,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
