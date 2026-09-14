# Aviation Accidents Data Engineering Project✈️

## The problem🔥

I wanted to know something specific: when a plane crashes, is there a
pattern behind why? Is it usually weather, is it mechanical failure, is
it the pilot, or is it something else entirely — war, hijacking,
mid-air collisions? I couldn't find a straightforward answer anywhere,
so I decided to build a pipeline that goes and finds it from real
historical crash records instead of guessing.

This isn't meant to be an aviation safety study — it's a data
engineering project, so the point is as much about building a proper
pipeline (raw data → cleaned data → classified data → queryable
database) as it is about the actual answer.

## The data

I'm using the [Airplane Crashes and Fatalities Since 1908 dataset from
Kaggle](https://www.kaggle.com/datasets/thedevastator/airplane-crashes-and-fatalities),
originally scraped from planecrashinfo.com. It covers 5,268 crashes
from 1908 to the present, with details like date, operator, aircraft
type, fatalities, and — most importantly for this project — a
free-text `Summary` field describing what happened in each crash.

The raw CSV isn't committed to this repo (it's excluded via
`.gitignore`) — grab your own copy from the Kaggle link above if you
want to run this yourself.

## How the pipeline works
Raw CSV → Clean → Classify cause → PostgreSQL → Analysis


**1. Ingest (`src/ingest.py`)**
Loads the raw CSV. Nothing fancy — just reads it in and confirms it
loaded correctly.

**2. Clean (`src/clean.py`)**
Fixes the date format (it comes in as plain text, not a real date),
fills in missing values for a few key fields, and drops columns that
don't matter for this problem (flight numbers, aircraft registration —
mostly missing anyway, and not relevant to figuring out *why* a crash
happened).

**3. Classify (`src/classify.py`)**
This is the actual core of the project. Since none of the source data
comes with a clean "cause" column, I built a keyword-matching system
that reads each crash's `Summary` text and assigns it to one of these
categories:

- **Hijacking/Sabotage** — bombs, hijackings, deliberate acts
- **War/Conflict** — shootdowns, combat losses
- **Mid-Air Collision** — two aircraft colliding (kept separate from
  everything else, since a summary rarely says *whose* fault a
  collision was)
- **Maintenance** — engine failures, structural failures, mechanical
  issues
- **Weather** — storms, icing, fog, turbulence, and similar
- **Pilot Error** — judgment errors, loss of control, stalls caused by
  pilot action
- **Unknown** — the summary explicitly says the cause was never
  determined, or there's no summary at all
- **Other** — a real summary that doesn't match any of the above

Since a lot of summaries mention more than one thing, categories are
checked in a specific priority order (unknown-cause statements first,
then hijacking/war/collision — since those are unambiguous when
mentioned — then maintenance, weather, and pilot error last). I went
through several rounds of pulling random samples of misclassified
summaries, reading them by hand, and expanding the keyword lists based
on real phrasing I found — not just guessing at words up front. Some
of that process is genuinely still visible in the numbers: for
example, "Unknown" jumped noticeably once I added an explicit check
for phrases like "cause undetermined," because I decided an explicit
statement that the cause was never found should win over guessing
based on some other word that happened to appear nearby.

**Known limitation:** around 40% of crashes land in "Other." I don't
think that's a flaw in the keyword logic at this point — a lot of
summaries in a 100+ year historical dataset are just terse facts
("Crashed shortly after takeoff") with no cause mentioned at all.
Forcing those into a category would mean inventing information the
data doesn't have.

**4. Load (`src/load.py`)** — *in progress*
Loads the classified data into PostgreSQL for querying.

**5. Analysis** — *not started yet*
Answering the actual question: how do these categories break down over
time, by aircraft type, by region?

## Tech stack

Python, pandas, PostgreSQL, SQLAlchemy, Jupyter — kept deliberately
simple. This project doesn't need a data warehouse or a distributed
database at this scale; local Postgres does the same job Redshift
would, just sized appropriately for one dataset and one person.

## Project structure

data/
raw/ - original CSV 
clean/ - cleaned data 
final/ - classified data, 
notebooks/ - exploratory analysis, sample checking
src/
ingest.py - loads raw data
clean.py - cleans and standardizes it
classify.py - assigns cause categories
load.py - loads into PostgreSQL


## Status

🚧 In progress. Ingestion, cleaning, and classification are working
end to end. Currently building the PostgreSQL loading step.