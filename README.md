# polling.gh Data Model Architecture (Django + Postgres + Docker)

## Table of Contents
...

***************************************************

## A. Context

## Data Models

### A. Geographic
```python
class GeographicalLevel(choices):
    Station=1
    Region=2
    Constituency=3
    National=4
```
1. **Polling Stations:** 
These are locations where people can cast their votes. A collection of these make up a constitent
```python
class Station(models):
    name=CharField()
    constituency=ForeignKey(Constituency)
```
2. **Constituency:** 
These are states in the country presided by a Senate Represenatative. A collection of these make up a region
```python
class Constituency(models):
    name=CharField()
    region=ForeignKey(Region)
```
3. **Regions:** 
These are states in the country presided by a Governor. A collection of regions make up the nation
```python
class Region(models):
    name=CharField()
    nation=ForeignKey(Nation)
```
4. **Nation:** 
This is the entire country rule by the President. Table must have a single record
```python
class Nation(models):
    name=CharField()
```
### C. Events
The election can be considered an event that has a start date and end date. Below are the required fields
```python
class Event(models):
    level=models.IntegerChoices(choices=GeographicalLevel)
    start_date=models.DateTime()
    end_date=models.DateTime()
```

### B. People

1. **Users:** Accounts to gain access to the app. NOTE: Given that this is an in-house polling tracker, all users MUST be from the client political party party.
```python
class User(models):
    email=models.EmailField()
    name=models.CharField()
    password=models.CharField()
    role=models.ChoicesField()
```


### B. Polling

1. **Party:** Party table is a list of all parties in the state.
```python
class Party(models):
    abbreviation=models.CharField()
    name=models.CharField()
```
2. **Positions:** This is a position, title or office being competed for in the election (presidency, vice presidency).
    
    + All available zones in all available levels are represented in the office. In other words, a record must be available for the nation, all regions and constituencies in this table
    
    + The table will map to the election results table as the parent table

    **Migration notes:**
    
    + In order to ensure integrity of the application, this table must be managed in party via migrations usign a preloaded list as well an admin panel to correct errors or enter new additions post migration
    
    + Application should include a **office tracker** that checks for offices with missing representatives from political parties.

```python
class Position(models):
    # name of the positon (cannot be changed after inital migration)
    name = models.CharField()
    # geo level (national, regional or consituency)
    level = models.ForeignKey(GeographicLevel)
    # actual zone the position resides over
    zone = models.IntegerChoices(choices=zone_choices)
    # election date
    event = model.ForeginKey(Event)
    
    @classmethod
    def zone_choices(cls):
        # do not include zones that have been set
        zone_ids = [d.zone_id for d in Position.objects.filter(level=cls.level, zone=cls.zone)]
        if cls.level == GeoLevel.nation:
            return Nation.object.exclude(zone_id__in=[1])
        elif cls.level == GeoLevel.region:
            return Region.object.exclude(zone_id__in=zone_ids)
        elif cls.level == GeoLevel.constituent:
            return Constituent.object.exclude(zone_id__in=zone_ids)


    @property
    def position(self):
        # get the actual positon title
        # e.g. Governor for the Volta Region
        pass
```

3. **Candidate:** This is a list of all candidates, their respective political parties and the offices they are in the race for.
```python
class Candidate(models):
    name=models.CharField()
    party=models.ForeignKey(Party)
    office=models.ForeignKey(Office)
```

4. **Results:** The results table tracks the performances of the party representatives in the various offices.
    + All results are captured as aggregate numbers ONLY at the polling station
    + Results are then collated up to get aggregate sums for constituents, regions and national
```python
class Result(models):
    '''
    Collates the total number of votes for each party for each office in each constituency. List of fields as follows:
        * office: office being vied for
        * station: the staton the votes were collected from
        * party: the party that votes were collected for
        * votes: total number of votes per constituent
        * file: path to the verification form
        * is_published: has to be vetted and publshed by regional agent before it can be used in results
    '''
    office = models.ForiegnKey(Office)
    station = models.ForiegnKey(Station)
    party = models.ForiegnKey(Party)
    votes = models.IntegerField(max_length=200)
    file = models.URLField()
    is_published = BooleanField(default=False)
```



***************************************************

## F. Setup and Configurations

***************************************************

## G. Resources

* Docker Compose with Django and Postgresql (deploy multi container with compose yml) https://kimlyvith.medium.com/docker-compose-with-django-and-postgresql-577739697b3f
* Django Rest Framweork https://www.digitalocean.com/community/tutorials/how-to-build-a-modern-web-application-to-manage-customer-information-with-django-and-react-on-ubuntu-18-04
* Frontend https://www.pluralsight.com/guides/how-to-use-react-to-set-the-value-of-an-input
