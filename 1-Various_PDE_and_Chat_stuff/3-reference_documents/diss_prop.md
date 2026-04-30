Dissertation Proposal

Deciphering the Talent Mosaic:

data-driven assessment of officer talent and unit-specific potential in
the US Army using complex networks

Charles R. Levine^1*,*2∗^

May 22, 2024

Dissertation committee

Albert-László Barabási (chair)

> *University Distinguished Professor; Northeastern University*

Alessandro Vespignani

> *University Distinguished Professor; Northeastern University*

Alexander Gates

> *Assistant Professor; University of Virginia*

Dakota Murray

> *Assistant Research Professor; Northeastern University*
>
> ^∗^email: levine.ch@northeastern.edu
>
> ^1^Network Science Institute, Northeastern University, Boston, MA
>
> ^2^Center for Complex Network Research, Northeastern University,
> Boston, MA

# Contents {#contents .TOC-Heading}

1 Introduction 1

2 Background 1

3 Literature Review 4

4 Datasets 8

4.1 The Person-Event Data Environment (PDE) 8

4.2 USMA commissioning lieutenant initial unit selections 9

5 Research Plan and Questions 9

5.1 Research Questions 10

6 Chapters 10

6.1 Chapter 1 10

6.2 Chapter 2 13

6.3 Chapter 3 15

7 Anticipating Challenges and Future Timeline 17

7.1 Wrangling the data and proxies. 17

7.2 Complex Computational methods. 17

7.3 Our intuition is wrong. 18

7.4 Timeline 18

8 References 19

9 Additional Figures 21

# Introduction

This study seeks to identify the influence of organizational and/or
individual fitness or *prestige* on individual success in the U.S. Army.
The Army is a large hierarchical enterprise and, like other large
organizations, functions as an intricate complex network comprising not
only employees, divisions, branches, and functional teams, but also
internal educational institutions as nodes. These internal schools exist
to prepare employees for new skill sets that may qualify them for
different operational specialties within the organization, or to enable
them to assume management roles at higher levels. Within this dynamic

framework, individuals, their current teams, and company educational
backgrounds form a triadic relationship, constantly influencing each
other. This complex temporal network underscores the interplay between
individual fitness and organizational prestige, making it difficult to
distinguish the external effects of affiliations from individuals\'
inherent abilities. By dissecting these interactions, we seek to
elucidate how affiliations with esteemed organizations or internal
educational institutions shape individuals\' trajectories and success
within the organizational ecosystem.

Most such institutions are embedded within the greater context of a much
larger labor market exerting multivariate influences, which complicate
the isolation of network phenomena. However, for this study we will
examine a large diverse organization made up of tens of thousands of
teams that uses an internal labor market model, essentially creating a
self-contained ecosystem where employees enter at the bottom level and
all promotions are exclusively from within. Further reducing bias and
refining the ecosystem for enhanced clarity, we will select an
institution where employees at the same level receive uniform
compensation irrespective of individual performance. We will accomplish
this by utilizing data provided by the US Department of Defense that
comprehensively tracks every soldier in the US Army for the last 24
years.

This proposal leverages people analytics, network science, and survival
analysis (Box-Steffensmeier et al. 2015; Hougaard 1995; Klein and
Moeschberger 2010) to contribute to talent management and assessment
reform, focusing on the DoD and the US Army, the world's largest
employer, as an exemplar. By integrating comprehensive longitudinal Army
personnel administrative data this study aims to develop and validate
quantitative measures for both unit prestige and social network
influence. These measures will then inform the creation of a predictive
model for officer career progression. Through three primary research
questions and associated case studies, our model can be used to
elucidate the nuanced dynamics influencing talent allocation, promotion,
and retention within the Army. Ultimately, this work seeks to inform
polices for leadership development and enhance talent management mission
success for industry, while averting the unintended departure of
exceptionally talented leaders due to oversights in their identification
and utilization.

# Background

On the eve of World War II, because of The Great War and The Great
Depression, the US Army was bloated with officers commissioned during
that war who were not mandated to retire until age 64. In 1940 General
George Marshall, with the authorization of congress, took complete
control over promotions and retirement dramatically culling the
mid-level to senior-level officer ranks, often replacing them with
previously much more junior officers based on talent instead of
seniority. After the war, however, the 1947 Officer Personnel Act (OPA)
instituted a new model known as "up or out," a drastic measure intended
to preclude a future similar bloat, resulting in virtually all officers
being managed not by talents but by a fixed, rank duration or
'time-in-grade' model aimed at identifying and selecting a small pool of
leaders for successively higher levels of command (Colarusso and Lyle
2014).

Traditionally, the US Army has focused on talent management by
prioritizing top performers. With no lateral entry at higher ranks, the
Army relies on early promotions, known as \"Below the Zone\" (BZ)
promotions, to acknowledge exceptional performance and potential.
Federal law limits BZ promotions to a small percentage of eligible
officers annually but in 1974, Secretary of the Army Calloway\'s
directive to maximize BZ promotions that year led to controversy.
Lieutenant Colonel Robert R. Hicks Jr. expressed opposition to this
expansion in his 1987 Army War College essay, advocating for BZ
promotions to remain exclusive to a select few officers who "truly meet
the qualifications." Hicks\'s eventual rise to the rank of general
underscores the prevailing policy of maintaining the status quo. He
commented, \"The morale of the officer corps was jeopardized during this
period as officers believed that too many officers were receiving a
promotion designed for an elite few."(Hicks 1987)

![](media/image2.jpeg)The Army's recent traditional career progression
model, outlined in the Defense Officer Personnel Management Act (DOPMA)
of 1980, predominantly involved annually commissioning second
lieutenants into cohorts known as officer Year Groups (YGs). These YG
cohorts form the basis for all future senior leadership selections
without provision for lateral entry. Although legally standardized, the
duration or 'time-in-grade' for each successive rank may be adjusted
annually with congressional approval. Over time, current or projected
organizational requirements may create an excess or shortage with
respect to the size of these cohorts as seen in Figure 2-1. The Army
Human Resources Command (HRC) is tasked with using methods to adjust
officer cohorts based on size, occupational specialty composition etc.,
to meet current or projected targets for the needs of the Army, to
include national mission requirements, fiscal resources, and national
policies. These adjustments usually take the form of changing
time-in-grade requirements and fitness standards for which officers in a
cohort are selected for promotion, or indirectly separation, each year.
Officer YGs advanced together on almost uniform schedules as the cohort
gradually attritted due to voluntary or involuntary separation ("up or
out") under an internal labor market model. Figure 2-1 also shows the
dwindling proportion of the original cohort authorized for continued
service, a forcing function that includes not only involuntary
separations of officers deemed low performers, but also voluntary
separation of talented high performers seeking other opportunities to
the organization's detriment.

![](media/image4.jpeg)As a result, following a standard career timeline
all YG officers are looked at for promotion by selection boards when
that YG has reached its templated time-in-grade, or "Primary Zone" (PZ),
as in Figure 2-2. For example, all officers commissioned as Second
Lieutenants in fiscal year 2002 are considered YG '02. These officers
will all be considered simultaneously in 2006 for promotion to Captain
by their PZ board at the end of the cohort's fourth year of service so
that those selected can be promoted in 2007. In general, officers not
selected for promotion are looked at again the following year and those
twice non-selected are involuntarily separated within 6 months
("Department of the Army Regulation 600-8-29 Officer Promotions" 2020).
The Army may also stand-up impromptu Officer Separation Boards (OSBs) as
in 2014 when the Army involuntarily separated about 8% of captains and
majors to meet mandated force strength drawdown goals for 2015.

The DOPMA conventional career model adopted a \'standard career path\'
from the OPA, with the objective of cultivating uniform officer
development to optimize the selection of leaders for a finite number of
coveted command positions. This approach yielded individuals who were
nearly homogeneous in terms of qualifications, skills, and experiences
as they progressed in their careers. However, the model fell short in
capturing detailed insights into individual officer Knowledge, Skills,
Behaviors and Preferences (KSB-Ps) ,focusing solely on adherence to
uniformly imposed training and experience standards. Not only did it
lack the flexibility to recognize and reward exceptional performance,
but it also had limited capability to acknowledge, much less record,
competence and success in specializations beyond those standardized for
preparing officers for command positions (Wardynski et al. 2010).

The Army's sees the way forward as moving from a data-poor,
industrial-age officer distribution system which distributes officers
based on manner of performance to an information-age talent management
system which matches officers based on officer KSB-P's gleaned from
their experiences (Army Talent Management Task Force 2019b). This marks
the shift from talent distribution to talent alignment where officers
are matched ![](media/image5.png)to available assignments based on their
unique KSB-Ps, as well as those of their organization in order to create
more effective programs to target the right talent, provide it with the
right developmental opportunities, and offer the right retention
incentives (Army Talent Management Task Force 2019a).

("STAND-TO! Army Talent Alignment Process" 2019)

# Literature Review

Central to our methodology is the recognition that success in the Army
encompasses more than individual attributes or skills; it is
significantly influenced by social signals from raters, peers, and units
that gauge an officer's fitness and reputation. While performance
represents the tangible outcomes of an officer's efforts, intrinsic
potential is seen as their capability for leadership within specific
roles and units, a quality that remains intangible. Ultimately, an
officer's success is interpreted through the organization's
acknowledgment, primarily reflected in the subjective evaluations
provided by raters and senior raters. Focusing on social signals reveals
two important complications. First, the interplay between individual
fitness and organizational reputation complicates the assessment of
their respective contributions to success (Burt 1992). Second, social
integration, essential for team performance (Page 2008), is inherently
influenced by biases, which can subtly influence the trajectory of
individual careers. Research shows that subjective signals, often
influenced by personal biases and limited perspectives, can lead to
suboptimal evaluations and homogeneity within groups. Conversely,
data-driven signals, characterized by their objective and measurable
nature, enable a more accurate assessment of situations, individuals,
and outcomes (Page 2008). Therefore, our goal is to pinpoint early
indicators of officer potential, performance excellence, and career
longevity. This involves analyzing how the Army's institutional
structure, organizational dynamics, and demographic biases shape
officers' career trajectories (Saling and Do 2020). The goal here is to
use network science tools to uncover algorithmically the role extrinsic
treatments versus intrinsic talents play in impacting the career
trajectory of officers. We concentrate on operationalizing the social
phenomenon of unit, school, or individual prestige as markers of
potential, performance, or success. By drawing parallels to previous
research on prestige in fields like science and visual arts, we aim to
shed light on its role in shaping career outcomes within the military
context. For example, in higher education faculty hiring is heavily
influenced by the prestige of the doctoral institution rather than
solely by academic merit or achievements (Clauset, Arbesman, and
Larremore 2015a). Rather than seeking causal explanations for these
dynamics, our exploratory data analysis approach highlights the specific
areas where causal experimental work could most effectively be
prioritized. Our data-driven analysis can help empower the transition to
a next generation model of officer development and recognition that
prioritizes individual knowledge, skills, behaviors, and preferences in
alignment with the demands of the digital age, enhancing talent
selection, development, employment, and retention.

The Army is a complex multilevel organization with both formal and
informal structures and hierarchies, forming a dynamic social network
that emerges from command, peer, and developmental dependencies among
troops. Recent research has highlighted the significant influences of
dyadic relationships between command leaders and their subordinates,
signaling various factors such as leadership style, mentorship,
guidance, and recognition. In their 2021 paper, Spain et al. employ
people analytics to show that battalion commanders have a strong effect
on the retention of their lieutenants after their initial Active-Duty
Service Obligation (ADSO). ![](media/image8.jpeg)Their focus was an
exploration of the relationship and its effects between Lieutenants,
freshly commissioned officers serving their first assignments and their
Battalion Commanders, second line supervisors who are senior officers
with approximately 18 years of service. Figure 3-1 shows this command
structure and relationship. Their hypothesis was that when initially
entering the Army, lieutenants often experience the influence of their
battalion commanders\' personalities, characters, or leadership styles
to a heightened degree. Using a multivariate regression statistical
model, they found that certain battalion commanders could be shown to
exert such a toxic influence on their initial entry lieutenants as to
make those lieutenants statistically more likely to leave the service
after their initial active-duty service obligation (ADSO) is over.
Likewise, some battalion commanders have the opposite effect: their
lieutenants are statistically more likely to remain in service beyond
their initial ADSO. In fact, they were able to show that whom their
first battalion commander was had more influence than all the other
co-variates examined. This effect was decidedly more pronounced on
high-performing lieutenants (E. Spain, Mukunda, and Bates 2021).

Their findings showed the dramatic effect these key leaders and their
leadership styles have on the future talent distribution of the
organization. Their data came from dyadic professional relationship
within battalions in the 1980s. The Battalion Commander Effect is a
ratio assigned to former battalion commanders that reflects the
proportion of lieutenants they commanded who remained in the service
after their ADSO, to the total number of lieutenants they commanded.
These relationships were notably weighted by duration of the influence.
Using the datasets that form the basis for our research we replicated
their approach. Examining the same group of specific battalions they
used, we used our engine to analyze more recent data. This distribution,
shown in Figure 3-2 provides some early insights. Most notably, Colonel
Spain found that the BCE ratio had standard deviation of approximately
$\sigma \approx \ 13\%$ . Our engine produced data reflecting a standard
deviation of $\sigma \approx 8\%$, reflecting a decrease in variance.
Although this is preliminary analysis, this result could be evidence
that the decrease in variation signals an increase in this effect on
lieutenants in the modern digital age. This illustrates the robustness
of our data and validates our ability to explore these dyadic
relationships at the next level looking at the larger professional
network to how those peer relationships among lieutenants and peer
battalion commanders may influence the system.

Likewise, using ordinary statistical methods, Lyle and Smith looked at
the probability that the Army promotes a captain early to the rank of
major based on whether the officer served as a
![](media/image10.png)company commander under a battalion commander that
the army also selected for early promotion to the rank of major. They
were able to show that if a lieutenant colonel battalion commander was
enough of a high performing officer as a captain to have been promoted
early to major (a below zone (BZ) promotion), then the company commander
captains directly under her are 29% more likely to be promoted early to
major themselves than those company commanders serving under non-BZ to
major battalion commanders. This effect also increased with the duration
of the tutelage (Lyle and Smith 2014). While these papers adeptly
explored the mentor-subordinate relationship within the common framing
of high performance and prestige, they fail to address systematic
multi-level structural influences. Network science offers a
sophisticated framework uniquely capable of capturing these structural
influences, thereby providing crucial insights into the forces and
decision heuristics that shape career trajectories. Using emergent data
science methods, we aim to empower the Army talent management reform
process, rendering the system's dynamics and biases transparent to both
Army leaders charged with talent management and the officers themselves,
thereby enhancing talent allocation, promotion, career satisfaction, and
mission accomplishment.

While evidence directly revealing the influences of social networks
beyond the dyadic influences of commanders and mentors is limited in the
Army context, findings from civilian organizational research suggest
that structural influences induced by interdependent teams and peer
groups are crucial for individual development and success. For example,
the success of employees in multilevel organizations is reflected in the
structure of their relationships (Contractor and Leonardi, Paul 2018),
and peer relationships are valuable to individual development (Kram and
Isabella 2017). Research also suggests that prior shared success among
team members is a strong predictor of future success, even more so than
the cumulative individual successes of team members (Mukherjee et al.
2019). This implies a benefit for longitudinal team continuity. While
company-size (80-250 persons) and battalion-size (280-600 persons)
organizations are given missions and operate as teams, Army teams
inherently lack the possible benefits of established prior teams'
successes because of churn. Army policy mandates an officer rotation,
resulting in significant turnover. Officers are usually reassigned to
different geographic duty stations every 2-3 years which most often
involves a physical family move to a different geographic location. In
addition, during those assignments, officers are frequently also
reassigned to different sub-units at that location. However, an
exception to this pattern arises when senior officers identify
subordinates with whom they have established a strong rapport or trust.
These senior officers may then submit \'by-name requests\' for these
subordinate officers to work under them in their new assignments,
although this practice is unofficial (Randel 2019). The use of Network
Science tools will enable empirical exploration of the effects of this
practice on officer careers and, potentially, mission success. This can
then be compared to civilian Network Science research that has shown
that creative careers are characterized by strong path dependence
(Fraiberger et al. 2018).

Finally, research on collective performance suggests that the
introduction of a high performing individual to a group can often have
negative effects on members' performance when relative incentives are in
place. An example of this is when workers' daily pay depends on the
ratio of individual productivity to average productivity among all
coworkers (Bandiera, Barankay, and Rasul 2005). The Army officer
evaluation system remains based on a form of stack ranking to fit a
forced distribution system that restricts the number of above average
evaluations raters and senior raters are allowed to give subordinates
(Evans 2018). When salary differentiation isn't an option, this
similarly creates purely relative incentives.

Our initial data exploration has shown that when following a YG cohort
of officers longitudinally through their careers, the running
proportional mean of above average ratings received by the cohort,
essentially the value of a top rating, seems to fluctuate according to
career milestones as shown in Figure 6-5. This phenomenon appears even
when compared across cohorts and specific time windows and warrants
further detailed exploration. As previously mentioned, in any evaluation
system where performance and potential fitness scores rely solely on
subjective rater input there exist biases which degrade true employee
valuation. The use of stack ranking adds an additional administrative
bias to the valuation. Research using discrete event simulations find
that this very policy of Army officer stack rankings induces a
disconnect between fitness evaluation and inherent performance
characteristics by as much as 24% (Evans and Bae 2019).

In conclusion, while the existing literature sheds light on the
significance of social networks and structural influences in civilian
organizations for career development and success, we see there is a
significant gap between contemporary human resource best practices and
the conventional Army talent management schema. Here, we aim to close
that gap by empowering the Army talent management revitalization with
new data science methods. Doing so could render the system's dynamics
and biases more transparent to both Army talent managers and the officer
corps. By analyzing the assignment trajectory of Army leaders within the
Army organizational social network, we can disentangle the topological
influences of social relationships along with optimizing for the
evolving operational environment. This clarity could in turn improve
talent allocation, promotion processes, and overall career satisfaction
within the Army.

# Datasets

We have obtained Institutional Review Board approval from The United
States Military Academy with our project deemed not human subject
research according to 32CFR219 (Project Control \# 22-015-1). In
addition, we have obtained concurrent Institutional Review Board
approval from Northeastern University with our project deemed not
research involving human subjects as defined by the Department of Health
and Human Services (IRB #21-12-15). Likewise, we will consult with DoD
Human Research Protection Office (HRPO) or the equivalent Army Research
Institute Review board for HSR Exempt concurrence.

## The Person-Event Data Environment (PDE)

![](media/image12.png)Until recently, Department of Defense personnel
data resided in a myriad of insular silos, making large-scale
comprehensive data-driven analysis infeasible. The challenge of data
ethics and infrastructure echoed a pervasive challenge across social
sciences worldwide (Lazer et al. 2020; Schneider, Lyle, and Murphy
2015). Forward thinking scientists in the DoD created a solution to
enable such research. Our primary data source is the \"Person-Event Data
Environment\" (PDE), a secure cloud-based repository specifically
designed to manage extensive digitized personnel data, including
financial, medical, training, deployment, and security system records
(Vie et al. 2015). Administered by the Research Facilitation Laboratory
(RFL) under the oversight of the Army Analytics Group (AAG), the PDE
provides a comprehensive timeline of each soldier's military journey,
from enlistment to discharge. The PDE datasets we are utilizing cover
every soldier in the Army, encapsulating 84 quarterly snapshot records
over 24 years to include approximately 200,000 officers, 38,000 warrant
officers, and 1.8 million soldiers and NCOs (Figure 4-1). The AAG has
already approved and provisioned in our AWS cloud environment the
following datasets: the Active-Duty Military Personnel Master (ACT-MAST)
with UIC and zip codes exposed, the Army Training and Requirements
Resource System (ATRRS) for military schooling information, the Army
Training Management System (ATMS), and the Military Entrance Processing
Command (MEPCOM) data.

![](media/image11.png)These datasets, through inventive exploratory data
analysis methods, have enabled us to infer thousands of command and peer
relationships to obtain preliminary results and a better understanding
of the organizational dynamic. Seeking more explicit granularity we
realized that actual performance evaluations could take our research to
the next level. After five years of dogged and persistent formal and
informal requests, we have finally obtained 6.9 million personnel
evaluation reports spanning 24 years, providing explicit discernment of
the subjective personal leader assessments of subordinate performance
and potential required to better approach causal relationship
understanding. These evaluations include Form DA 67, Officer Evaluation
Reports (OERs) from the Army Single Evaluation Processing System (SEPS)
which explicitly identify employees, raters, senior raters, units to
which they belong, duration of rating periods, job titles during the
rating period, and rater and senior rater assessments (Figure 4-2). This
amazing dataset now allows creation of directed Officer Professional
Networks that provide a treasure of rich nodal and link metadata that,
unlike other many past methods of data exploratory analysis, allow the
networks to speak to us graphically, showing where to look to discover
new underlying hidden rules and dynamics. By integrating disparate Army
and Department of Defense (DoD) databases, the PDE creates a centralized
repository exceeding traditional Big Data benchmarks, ensuring data
security while enabling in-depth analysis.

## USMA commissioning lieutenant initial unit selections

Our secondary dataset is the graduating cadet initial unit selections
(Post Night) obtained from the US Military Academy at West Point. This
data involves approximately 1,000 graduating cadets yearly for multiple
cohort years. Annually, cadets are ranked on an Order of Merit List
(OML) and given a list of unit assignments with a limited number of
slots per unit. Cadets choose their unit assignments based on their OML
ranking, starting with the highest-ranked cadet, giving top preference
to top performers. Our data includes the OML and corresponding cadet
unit choices. The OML is only partly based on academic performance.
Rather than purely academic ranking, the West Point OML is a
conglomeration of academic, military, and physical performance. Research
has shown that for West Point graduates, cognitive ability alone is a
negative predictor of officer career success in both the short term and
longer term (E. S. Spain, Lin, and Young 2020).

# Research Plan and Questions

Here, we propose to leverage comprehensive administrative data capturing
the careers of 201,038 Army officers over 24 years combined with
graduating USMA cadet initial unit selections (i.e., USMA's "Post
Night") to develop holistic models of Junior Leader Competencies and
career progression through components, branches, assignments, and units.
These models will empower us to measure the interplay among unit, peers,
and evaluators and discern their respective impacts on the career
trajectory of officers, isolating the signals of intrinsic talent from
extrinsic treatments. This project is operationalized through three
primary questions which sequentially integrate metrics for unit
prestige, peer fitness, and rater evaluations, and are validated through
five case studies. These three primary research questions form the
backbone of each chapter of this proposed dissertation, as outlined in
Section 6.

## Research Questions

Q 1 *How effectively do network methods capture the prestige of
organizational units and schools, which attract more talent and signal
future success compared to conventional organizations? Moreover, does
this vary across officer demographics?*

Q 2 *What are the social network effects of serving alongside
prestigious peers on officer careers? Do these effects differ across
officer demographics?*

Q 3 *What are the trade-offs between prestige unit service and fitness
recognition from raters and senior raters in predicting career success?
Do these effects differ demographically?*

# Chapters

## Chapter 1

Q1: *How effectively do network methods quantitatively capture
prestigious organizational units and schools, which attract more talent
and signal future success compared to conventional organizations?
Moreover, does this vary across demographic factors?*

![](media/image16.jpeg)We seek first to derive a metric that collapses
the multivariate complex organizational effects of individual unit
service into a single scalar value: the unit prestige. Institutional
prestige is difficult at best to objectively measure and is complicated
by the fact that it depends on interactions between institutions and on
subjective evaluations, among other factors (Clauset, Arbesman, and
Larremore 2015b). For this reason, our core approach will be to use
network methods and attempt to validate computed metrics with a
different computational method using different data. Following
Fraiberger et al. 2018, we build the infinite time horizon Officer
Career Network (OCN). In the OCN, network vertices are commands and
units, and two units are linked by a directed edge if an officer was
assigned first in the source unit before being assigned to the target
unit later in his or her career. The infinite time horizon specifies no
cutoff is used in the connections induced by careers (Fraiberger et al.
2018). Since our data provides unit information down to the company
level, we can use individual companies as nodes or aggregate to
battalion, brigade, division, or all the way up to the combatant command
level to build temporal vectors from the organizational career path
walks of these officers. The hierarchical structure of the Army and the
Unit Information Codes (UICs) it uses to identify units according to
that structure lends itself to aggregations that can represent
arbitrarily sized and grouped organizations as "community" nodes. This
arbitrary granularity enables our network engine to test previously held
anecdotal as well as empirical claims about organizational influence on
individual success. An example of an Army Career Network with company
level organizations is shown in Figure 6-1. An initial analysis reveals
the presence of organizational communities (one example highlighted)
corresponding to specialty in which soldiers became locked. In this
diagram we see a special that a newly formed training unit created a
small community of skill specific professionals such that these same
specialists spent the rest of their careers in what might be considered
a "prestige" community. This initial impression of gained from graphical
representation that perhaps unintended or even unrecognized communities
seem to have formed was then later confirmed when computational
![](media/image18.png)analysis revealed the network has a relatively
high modularity score of 0.833.

Although based on what may be perceived to be a rigid hierarchical
system, preliminary OCN constructions are by no means uniform. In fact,
preliminary degree distribution analysis shows an exponential gamma of
2.319, classifying the OCN as scale-free (Barabási and Albert 1999) as
visualized in Figure 6-2. We quantify the prestige of organizations
based on their eigenvector centrality in the OCN. Eigenvector centrality
is a measure of node influence based on the principle that connections
to high-scoring nodes contribute more to the score of the node than
equal connections to low-scoring nodes (Newman 2016). In the context of
the OCN, this metric integrates over all officer careers and their
units, quantifying the propensity for service in a unit to signal future
service in other prestigious units. To maximize understanding of unit
network importance we will investigate both first and second
eigenvectors (Iacobucci, McBride, and Popovich 2017).

> To validate our measure of unit prestige, we apply it to three
> hypotheses:

*H1a: Higher talent USMA junior officers will disproportionately choose
prestigious units.*

First, since the highest performing cadets at USMA receive their first
choice, the order in which units were chosen should reflect the prestige
with which they are regarded by entry officers. We will group officers
by unit choice and then average their OML ranking reciprocals to create
prestige indexes for each unit building a normalized vector. This will
be compared with the eigenvector centrality vector using Cosine
similarity and Pearson correlation. We expect that junior officers
believe that some units are more prestigious than others. We expect that
this computed metric of prestige will closely match and validate the
network eigenvector centrality method of measuring prestige among
organizations.

*H1b: Officers that serve in prestigious units, such as the Ranger
Regiment, will be promoted earlier to Major, Lieutenant Colonel, and
Colonel than their peers who have not.*

Second, we associate each officer with the number of days spent as
Captain and Major to discover distributions of time-in-grade for
officers with and without experience in prestige units as lieutenants.
We expect that prestige organization veterans may experience earlier
promotion rates than officers without that experience, and we expect the
difference in time-in-grade distributions will be statistically
significant using Welch's t-test. We will then build a Cox Proportional
Hazards model to capture the influences of demographics, training, and
prestige on survival times to promotion while accounting for the effects
of the Army's often annual manipulation of cohort year group size.

*H1c: Company commanders that have graduated from prestigious schools,
such as Ranger School, will spend longer in company command than their
peers who have not.*

Third, we validate our prestige measure for Army schools based on the
subsequent duration of company command. The Key and Developmental (KD)
assignment for captains in most Army career fields or Military
Occupational Specialties (MOSs) is command of a company. Company command
occurs within about two years after officers are promoted to captain,
about 5-7 years into their careers. Companies vary in size from 80-250
officers, NCOs and soldiers depending on the unit type with the mean
size being about 130 personnel. The optimum length of command tours will
be based on the needs of the Army, stability within units, need for
officers with command experience, and availability of personnel
("Department of the Army Regulation 600-20 Army Command Policy" 2020).
HRC templates command tour duration targets designed to maximize command
opportunity across the force. Captains who are considered top performers
in command traditionally will be allowed to stay in command longer or
even get a second command of a different unit. Opportunities for longer
and second commands are uniformly scarce across all organizations.
Current Army standards for company command time are minimum 12 months,
with 18 months being ideal. HRC tries to limit command time to 24 months
maximum. These numbers have varied over time, but the ratios remain the
same for year group cohorts. Based on the availability of longer command
time and the number of commanders in a battalion that compete for it, a
preliminary estimate is that 25% of company commanders in a battalion
will be able to get longer command. Using the same methods as above, we
will examine the correlation of prestige schooling with longer company
command time among year group cohorts, a signal of individual high
performance and potential.

## Chapter 2

Q2: *What* *are the* *effects* *of serving alongside prestigious peers
on officer careers?* *Do these effects differ
demographically?*![](media/image20.jpeg)

![](media/image22.jpeg)Here we seek to uncover how the social network
can confound the earlier prestige treatment effects we investigated. The
Officer Professional Network (OPN) is generated temporally from the OCN
using unit co-location officer relationships weighted by duration. In
this network vertices represent individual officers, and edges are built
as social ties when assignment colocation and duration are considered.
This approach allows for directed edges as well to explore the effects
of command relationships and peer influences. For example, an
operational battalion commander will have five captain company
commanders serving directly under her. She will have a directed edge
relationship to each of her commanders, and they will have peer
undirected edges to each other with edge weights all being determined by
the duration of serving together. An example of a longitudinal OPN
between officers when serving as company and battalion commanders is
shown in Figure 6-3. This network, depicting thousands of individual
battalions over twenty years' time, reveals command *chains* as some
company commanders later become battalion commanders themselves. Figure
8-1 shows the command chain relationships that form among officers in
Forces Command (FORSCOM), the major Army command responsible for
operation units, separate from the rest of the Army HQ in the top right.
Another OPN, tracking the relationships over time between the battalion
commanders and their lieutenants in the Spain paper over a twenty-year
period shows a Poisson degree distribution as seen in Figure 6-4. What
we would expect to see here is much less variance. This organization is
one in which both career progression and organizational structure seem
anecdotally very prescribed and in addition we have chosen an
organization that is a closed system, free from outside entry. Instead,
what we see is that some leaders and some junior officer can have widely
different experiences in terms of how many other officers they will
influence and be influenced by in their careers. Historically, research
on officer career paths has relied on aggregating lists and creating
multivariate regression models. In addition, more recently my colleagues
and mentors in the Army Operations Research and System Analysis (ORSA)
community have created stochastic block models to predict HR trends and
analyze dynamics (Dabkowski et al. 2010).

The discussion surrounding talent in the Army often overlooks the impact
of peer talent on officers serving together. When officers of the same
rank are in the same unit, they not only serve as professional peers but
also share the same chain of command, including the same commander and
senior rater. While peer evaluations are utilized extensively in Army
training and development, literature focusing on peer effects rather
than mentorship effects is limited. In exploring the influence of peer
talent on success, it becomes evident that officers in the same unit
compete for top evaluations within the Army evaluation system. This
competition is heightened when peers share the same chain of command,
emphasizing the importance of understanding how working alongside
average or high-performing officers affects individual success.
Anecdotally, seeking admission to prestigious organizations to serve
alongside top performers is believed to positively impact an officer's
career. This belief finds support in civilian literature on peer
development and previous military literature on mentorship.

The Army personnel records system is primarily designed to identify a
soldier's supervisor and senior rater, with little attention devoted to
recording the soldier's peers. However, the Officer Professional Network
we have constructed provides us with the capability to quickly ascertain
unit members and chains of command at various echelons for both
prestigious and typical organizations across the Army. This network
spans the longitudinal career paths of Army officers, revealing the
intricate connections among units, leaders, and careers. Such
information is indispensable for uncovering the effects of peer
relationships on perceived performance and the ultimate success of
officers It will be interesting to see if there is a peer talent paradox
analogous to the friendship paradox.

*H2: Ranger school graduate company commanders in a prestige unit tend
to have shorter tenure in company command compared to their peers in
typical units.*

Earlier we hypothesized that Company commanders that have graduated from
prestigious schools, such as Ranger School, will spend longer in company
command, a signal of high performance, than their peers who have not.
When analyzing high-performing officers throughout the Army, it becomes
evident that command duration opportunities are uniformly restricted
irrespective of the unit. Battalion commanders in prestigious
organizations have the same command opportunities to offer their
talented captains as do battalion commanders in typical units.
Consequently, officers stationed in prestigious organizations with
higher talent density are likely to encounter fewer opportunities for
extended command tenure compared to their equally fit peers in more
conventional units. We think that we will find that a hidden paradigm is
that the positive career effects enjoyed by those officers attending a
prestigious school will not be as likely to be realized if those
officers are serving in a prestigious unit. To quantify this phenomenon,
we will employ survival modeling techniques to discern disparities in
command duration between prestigious and typical organizations.
Furthermore, we will pair officers commanding in both prestigious and
typical units, controlling for other relevant factors, and utilize the
OPN to construct their ego and alter networks. This will enable us to
measure and compare the average command duration of their closest peers.
We will investigate whether these results vary according to officer
demographics, and if so, what are the predictors of this paradigm having
a greater or lesser effect.

## Chapter 3

Q3: *What are the tradeoffs between prestige unit service and fitness
recognition from raters and senior raters in predicting career success?
Do these* *effects differ demographically?*

Finally, we extend our investigation of prestige treatments to examine
the effect of peer talent on rater and senior rater evaluations of
performance for captains commanding companies in both prestige and
typical units. Published conventional wisdom states that officer success
is purely dependent on performance and should not be affected by unit
prestige \[22\]. However, career officers share widely different
opinions of this statement, and HR professionals who administrate the
new unit assignment process document that some units are
disproportionately requested in the new assignment process (United
States Army Human Resources Command (institution), n.d.). Here we
leverage the Army Officer Evaluation Reports (OERs) to differentiate
officers of the same rank in the same unit. Like longer command time,
top ratings are limited and closely monitored. Raters and senior raters
have a recorder running rating 'profile" that HRC closely tracks to
prevent rating inflation. Service in a prestige organization with a
greater talent density than a typical one therefore should in the short
term make high performers less statistically likely to receive top marks
than their equally talented peers in less competitive talent pools. On
the other hand, later in their careers early prestige unit service may
make them more competitive for battalion command, perhaps the most
decisive signal of success for career officers with less than 20 years
of service. We will investigate whether these results vary according to
officer demographics, and if so, what are the predictors of this
paradigm having a greater or lesser effect.

The OERs provide space for narrative text for both the rater and senior
rater evaluating military officers' performance and potential. In
addition, evaluators also must indicate performance and potential
through a discrete set of ordered categories, in this case boxes they
check. These "box checks" carry significant weight with promotion and
selection boards. By combining box checks with unit prestige, we can
re-frame our central question to ask: "Is it more advantageous for
long-term career success to occupy a prominent position within a typical
unit or a less prominent position within a prestigious unit?" Figure 6-5
tracks the average number of top blocks over time that members of the
officer commissioned in 2001 in proportion to the total number of
evaluations given across the Army for that cohort of officers. That
running mean is graphed longitudinally in conjunction with the Army
Officer career model below it. What we see graphically are trends that
seek explanation and clearly must illuminate the network dependency of
individual success, showing we have just begun to obtain unique insights
as to the meaning and true value of these subjective network signals on
officer career success. The construction of the OPN allows us insight as
to what part institutional and peer prestige might play in this
unexpected variation.

*H3: Company commanders who receive top box checks in typical units will
be more likely to receive early field grade promotions than their
counterparts who receive median box checks commanding in prestigious
units.*

![](media/image17.png)To test this, we will compare future success of
officers commanding in prestige and non-prestige organizations who
received top rater and senior rater box checks respectively on command
OERs to those who did not. Like limited second command opportunities,
rater and senior rater evaluation box checks have a forced distribution
("Department of the Army Regulation 623-3 Evaluation Reporting System"
2019), therefore we suspect that prestige unit commanders should have
lower mean fitness evaluations than their peers of equal talent
commanding in more typical organizations. We will create and compare
survival curves for service retention and early promotion to field
grades to discover the extent that prestige unit command time confounds
the box check influence on success using the above listed methods. To do
this we will use PDE ACT-MAST and SEPS OER data for YG cohorts. In
addition to longer company command as captains, we have identified that
early promotion to major and lieutenant colonel

# Anticipating Challenges and Future Timeline

## Wrangling the data and proxies.

![](media/image26.png)Some of the metrics that we need to identify
aren't easily accessible. For example, one of our metrics of success is
early promotion to major. This was the pivotal metric in the Lyle paper
on mentorship. While the Army publishes the promotion selection lists
every year for all ranks, that data is not in our dataset. Even if it
were those lists until recently did not explicitly denote which officers
were being promoted below the zone or above the zone (early or late).
Our data does, however, tell us the number of months each officer spent
at each grade. Remember that time-in-grade standards can change from
year to year. To identify early promotion, we grouped officers by YG
cohort. Then we needed to eliminate officers with non-standard career
timelines like legal and medical professionals which could potentially
introduce bias into our analysis. Next, we computed distributions for
number of months spent in each rank for each year group. We then plotted
those distributions expecting to see a bi-modal distribution. There
should be a tall curve representing the mean of those officers promoted
PZ, or on time, and there should be a smaller curve in front for those
promoted early. We then drew a 'BZ' line between the two and decided
time in grade less that that line was early promotion as shown in Figure
7-1. Until we obtained the OERs we had to rely on proxies to infer
command relationships. Knowing all officers assigned to each unit each
quarter, and knowing their ranks at the same time, we knew that if a
Unit Identification Code (UIC) ended in 'T0' it meant that it was a
battalion headquarters. There should be one lieutenant colonel assigned
to a battalion headquarters, and he should be the battalion commander.
This is not always reflected in the data. UICs are nested so that the
first four digits, or prefix, are the same for all units within the
battalion or brigade level command. We can then identify the UIC's that
should fall under that battalion headquarters, and those companies
should have one captain and that should be the company commander. The
data of course isn't that clean. Often there are two lieutenant colonels
in the HQ. Most of the data is quarterly snapshots, four per year. We
then wrote code to examine previous and subsequent quarters to see if
there was just an overlap during command transfer. All these proxies
introduce error. The more circuitous the route, the more error is
introduced and perhaps the less we can trust our results.

## Complex Computational methods.

We plan to make use of Survival Analysis to model the time between being
promoted to captain and being promoted to major to better understand
time-in-grade. With this method we will use the Kaplan Meir estimator,
the Cox Proportional Hazards Model, and the logrank test. We have some
good papers from the National Institute of Health to use as models. Even
with those papers this will be challenging.

## Our intuition is wrong.

The biggest challenge is that, despite what we hypothesize and expect to
be true, our results may point in a different direction. The dataset is
very large. Most of our metrics involve significant computation. Metrics
we create may not accurately reflect what we are trying to measure, and
confirmation bias may obscure this. Defining what constitutes valid
computational success will be challenging.

## Timeline

We expect to have these research questions answered, the dissertation
written, and ready for defense in the spring semester.

# References

Army Talent Management Task Force. 2019a. "Army Talent Alignment
Process." STAND-TO! October 16, 2019.
https://www.army.mil/standto/archive/2019/10/16/.

---------. 2019b. "Army Talent Management at AUSA 2019 \| Article \| The
United States Army."
https://www.army.mil/article/228463/army_talent_management_at_ausa_2019.

Bandiera, Oriana, Iwan Barankay, and Imran Rasul. 2005. "Social
Preferences and the Response to Incentives: Evidence from Personnel
Data." *The Quarterly Journal of Economics*, August, 917--62.
https://doi.org/10.1093/qje/120.3.917.

Barabási, Albert-László, and Réka Albert. 1999. "Emergence of Scaling in
Random Networks." *Science Magazine* 286 (October):509--12.

Box-Steffensmeier, Janet M., Raphael C. Cunha, Roumen A. Varbanov, Yee
Shwen Hoh, Margaret L. Knisley, and Mary Alice Holmes. 2015. "Survival
Analysis of Faculty Retention and Promotion in the Social Sciences by
Gender." *PLoS ONE* 10 (11): e0143093.
https://doi.org/10.1371/journal.pone.0143093.

Burt, Ronald S. 1992. "Structural Holes: The Social Structure of
Competition." *The Social Structure of Competition*.

Clauset, Aaron, Samuel Arbesman, and Daniel B. Larremore. 2015a.
"Systematic Inequality and Hierarchy in Faculty Hiring Networks."
*Science Advances* 1 (1): e1400005.
https://doi.org/10.1126/sciadv.1400005.

---------. 2015b. "Systematic Inequality and Hierarchy in Faculty Hiring
Networks." *Science Advances* 1 (1): e1400005.
https://doi.org/10.1126/sciadv.1400005.

Colarusso, Michael J, and David S Lyle. 2014. *Senior Officer Talent
Management: Fostering Institutional Adaptability*. Carlisle, PA:
Strategic Studies Institute and U.S. Army War College Press.

Contractor, Noshir, and Leonardi, Paul. 2018. "Better PEOPLE Analytics
Measure Who THEY KNOW, Not Just Who THEY ARE." *Harvard Business
Review*, November 1, 2018.
https://hbr.org/2018/11/better-people-analytics.

Dabkowski, Matthew F., Samuel H. Huddleston, Paul Kucik, and David Lyle.
2010. "Shaping Senior Leader Officer Talent: How Personnel Management
Decisions and Attrition Impact the Flow of Army Officer Talent
throughout the Officer Career Model." *Proceedings - Winter Simulation
Conference*, no. December 2010, 1407--18.
https://doi.org/10.1109/WSC.2010.5679052.

"Department of the Army Regulation 600-8-29 Officer Promotions." 2020.
Department of the Army.
chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN30301-AR_600-8-29-000-WEB-1.pdf.

"Department of the Army Regulation 600-20 Army Command Policy." 2020.
Department of the Army.
https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN32931-AR_600-20-004-WEB-6.pdf.

Evans, Lee A. 2018. "Simulation-Based Analysis and Optimization of the
United States Army Performance Appraisal System." University of
Louisville.

Evans, Lee A., and Ki Hwan G. Bae. 2019. "US Army Performance Appraisal
Policy Analysis: A Simulation Optimization Approach." *Journal of
Defense Modeling and Simulation* 16 (2): 191--205.
https://doi.org/10.1177/1548512918787969.

Fraiberger, Samuel P., Roberta Sinatra, Magnus Resch, Christoph Riedl,
and Albert-László Barabási. 2018. "Quantifying Reputation and Success in
Art." *Science* 362 (6416): 825--29.
https://doi.org/10.1126/science.aau7224.

Hicks, Robert R. 1987. "The Below the Zone Promotion System."
https://apps.dtic.mil/sti/citations/ADA180153.

Hougaard, P. 1995. "Frailty Models for Survival Data." *Lifetime Data
Analysis* 1 (3): 255--73. https://doi.org/10.1007/BF00985760.

Iacobucci, Dawn, Rebecca McBride, and Deidre L. Popovich. 2017.
"Eigenvector Centrality: Illustrations Supporting the Utility of
Extracting More Than One Eigenvector to Obtain Additional Insights into
Networks and Interdependent Structures." *Journal of Social Structure*
18 (1): 1--23. https://doi.org/10.21307/joss-2018-003.

Klein, John P. P., and Melvin L. Moeschberger. 2010. *Survival Analysis:
Techniques for Censored and Truncated Data*. New York, NY: Springer.

Kram, Kathy E., and Lynn A. Isabella. 2017. "Mentoring Alternatives: The
Role of Peer Relationships in Career Development." *Academy of
Management Journal*, November. https://doi.org/10.5465/256064.

Lazer, David M. J., Alex Pentland, Duncan J. Watts, Sinan Aral, Susan
Athey, Noshir Contractor, Deen Freelon, et al. 2020. "Computational
Social Science: Obstacles and Opportunities." *Science* 369 (6507):
1060--62. https://doi.org/10.1126/science.aaz8170.

Lyle, David S., and John Z. Smith. 2014. "The Effect of High-Performing
Mentors on Junior Officer Promotion in the US Army." *Journal of Labor
Economics* 32 (2): 229--58. https://doi.org/10.1086/673372.

Mukherjee, Satyam, Yun Huang, Julia Neidhardt, Brian Uzzi, and Noshir
Contractor. 2019. "Prior Shared Success Predicts Victory in Team
Competitions." *Nature Human Behaviour* 3 (1): 74--81.
https://doi.org/10.1038/s41562-018-0460-y.

Newman, Mark E. J. 2016. *Networks: An Introduction*. Reprinted. Oxford:
Oxford University Press.

Page, Scott. 2008. *The Difference: How the Power of Diversity Creates
Better Groups, Firms, Schools, and Societies - New Edition*. Revised
edition. Princeton, NJ: Princeton University Press.

Randel, Brennan. 2019. "The Army Has a Revolutionary New Talent
Management System. Now We Have to Make It Work." Modern War Institute.
December 23, 2019.
https://mwi.westpoint.edu/army-revolutionary-new-talent-management-system-now-make-work/.

Saling, Kristin C., and Michael D. Do. 2020. "Leveraging People
Analytics for an Adaptive Complex Talent Management System." *Procedia
Computer Science* 168:105--11.
https://doi.org/10.1016/j.procs.2020.02.269.

Schneider, By Karl F, David S Lyle, and Francis X Murphy. 2015. "Framing
the Big Data Ethics Debate for the Military." *Jfq 77*, no. 2nd Quarter,
16--23.

Spain, Everett, Gautam Mukunda, and Archie Bates. 2021. "The Battalion
Commander Effect," 15.

Spain, Everett S., Eric Lin, and Lissa V. Young. 2020. "Early Predictors
of Successful Military Careers among West Point Cadets." *Military
Psychology* 32 (6): 389--407.
https://doi.org/10.1080/08995605.2020.1801285.

Vie, Loryana L., Lawrence M. Scheier, Paul B. Lester, Tiffany E. Ho,
Darwin R. Labarthe, and Martin E.P. Seligman. 2015. "The U.S. Army
Person-Event Data Environment: A Military--Civilian Big Data
Enterprise." *Big Data* 3 (2): 67--79.
https://doi.org/10.1089/big.2014.0055.

Wardynski, Casey, David S Lyle, Michael J Colarusso, Army War College
(U.S.), and Strategic Studies Institute. 2010. *OFFICER CORPS STRATEGY
SERIES TOWARDS A U.S. ARMY OFFICER CORPS STRATEGY FOR SUCCESS: RETAINING
TALENT*. OFFICER CORPS STRATEGY SERIES.
http://books.google.com/books?id=Wn0YAQAAMAAJ.

# ![](media/image21.png)Additional Figures

# 
