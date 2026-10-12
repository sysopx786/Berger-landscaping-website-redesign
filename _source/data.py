import re, json, os

SITE = "https://www.bergerlandscaping.net/"
# Quote form: FormSubmit standard endpoint (not /ajax/, which drops file attachments).
# Pitch/testing inbox; switch to drew@bergerlandscaping.net after approval.
FORM_ENDPOINT = ""  # blank = quote form hidden. To turn on: "https://formsubmit.co/<inbox email>"
BIZ = dict(
    name="Berger Landscaping LLC", short="Berger Landscaping",
    phone="(610) 420-3338", tel="+16104203338",
    email="drew@bergerlandscaping.net",
    street="110 Holby Lane", city="Pottstown", region="PA", zip="19465",
    fb="https://www.facebook.com/profile.php?id=100094171704575",
    fb_photos="https://www.facebook.com/profile.php?id=100094171704575&sk=photos",
    gmaps="https://maps.app.goo.gl/VcP8FdZ8u5XwiSSY7",  # Google listing / reviews (owner-supplied)
    greview="https://maps.app.goo.gl/hmSA2zj3VKHFWFtV6",  # Google "write a review" (owner-supplied)
    gdir="https://www.google.com/maps/dir/?api=1&destination=110+Holby+Lane+Pottstown+PA+19465",
    gembed="https://www.google.com/maps?q=110+Holby+Lane,+Pottstown,+PA+19465&output=embed",
    area="Southeastern Pennsylvania",
)

# ---------- FAQs parsed from the source file ----------
def parse_faqs(path):
    txt = open(path, encoding="utf-8").read()
    groups = {}
    for m in re.finditer(r"^## (\d+)\. (.+?)\n(.*?)(?=^---|\Z)", txt, re.S | re.M):
        name = m.group(2).strip()
        items = re.findall(r"\*\*\d+\. (.+?)\*\*\n(.+?)(?=\n\n|\Z)", m.group(3), re.S)
        groups[name] = [(q.strip(), a.strip()) for q, a in items]
    return groups

FAQS = parse_faqs(os.path.join(os.path.dirname(os.path.abspath(__file__)),"berger-landscaping-faqs.md"))
assert len(FAQS) == 10 and all(len(v) == 15 for v in FAQS.values()), {k: len(v) for k, v in FAQS.items()}

# ---------- Services (description copy verbatim from notes) ----------
SERVICES = [
 dict(slug="mowing", name="Mowing", icon="mowing", season=None,
  card="Clean, even cuts on a set schedule, including big lawns and steep hills.",
  promise="Clean, consistent cuts on a regular schedule, including large lawns and steep hills.",
  desc=["A well-kept lawn is the foundation of a beautiful property. Our mowing service delivers clean, consistent cuts on a regular schedule, so your lawn stays healthy, even, and inviting all season long.",
        "Each visit includes mowing, edging along walkways and beds, trimming around obstacles, and blowing clippings off driveways and hard surfaces. We cut at the right height for your grass type, which helps it grow thicker, resist weeds, and handle summer heat.",
        "We also take on challenging properties, including large lawns and steep hills. Whether you manage a home, a business, or a multi-living community, we show up on time and leave your property looking its best."],
  draft=True,
  included=["Mowing at the right height for your grass type","Edging along walkways and beds","Trimming around beds, trees, fences, and other obstacles","Clippings blown off driveways and hard surfaces","Large lawns and steep hills"],
  photos=["berger-lawn-04","berger-lawn-03","berger-lawn-07"],
  tip=("After rain","If it rains on your mowing day, we move the cut to the next suitable day. Cutting very wet grass can tear it and leave ruts."),
  related=["property-maintenance","aeration-sod-seeding","yard-clean-up"]),
 dict(slug="property-maintenance", name="Property Maintenance", icon="property", season=None,
  card="Ongoing care for lawns, beds, shrubs, trees, and common areas.",
  promise="Year-round upkeep that keeps homes, businesses, and communities clean, safe, and good-looking.",
  desc=["Property maintenance ensures that every outdoor space (whether a residential home, commercial business, or multi-living community) remains clean, safe, and visually appealing throughout the year. It includes the ongoing care of lawns, landscape beds, shrubs, trees, hardscapes, and common areas to protect your investment and keep the property looking its best in every season.",
        "From routine mowing and trimming to seasonal cleanups, mulch installation, and debris removal, property maintenance provides consistent, reliable upkeep that enhances curb appeal and supports long-term landscape health."],
  included=["Routine mowing and trimming","Seasonal cleanups","Mulch installation","Debris removal","Care of landscape beds, shrubs, trees, hardscapes, and common areas"],
  photos=["berger-beds-12","berger-beds-20","berger-hardscape-05"],
  tip=("Plans that change","Your needs change with the seasons, and the plan can change with them. Add or adjust services as the year goes on."),
  related=["mowing","yard-clean-up","custom-landscaping"]),
 dict(slug="custom-landscaping", name="Custom Landscaping Solutions", icon="custom", season=None,
  card="Designs built for your property, made to manage runoff, weeds, and pests.",
  promise="Personalized designs that look good and are planned to reduce runoff and support natural weed and pest control.",
  desc=["Our professional services go beyond aesthetics. Our careful and detail-oriented designs are tailored to minimize rainwater runoff and support natural weed and pest control.",
        "Studies have shown that these enhancements can not only increase your home value by up to 12%, but landscaping can also have a positive impact on your mental well-being!"],
  included=["Designs personalized to your property and your input","Planning to minimize rainwater runoff","Designs that support natural weed and pest control","Removal of existing plants and shrubs where the plan calls for it","Ongoing maintenance available after installation"],
  photos=["berger-hardscape-03","berger-hardscape-06","berger-beds-22"],
  tip=("Build in phases","Larger plans can often be broken into stages, so you can build the landscape over time."),
  related=["property-maintenance","trimming","yard-clean-up"]),
 dict(slug="aeration-sod-seeding", name="Aeration, Sod & Seeding", icon="seed", season="Spring · Fall", draft=True,
  card="Core aeration, overseeding, seed, and sod to thicken a thin lawn or start a new one.",
  promise="Thicker, healthier turf, whether you're patching bare spots or starting a lawn from bare soil.",
  desc=["A strong lawn starts below the surface. Whether you're starting from bare soil or bringing back a thin, patchy yard, the results depend on how well the ground is prepared and how the new grass is cared for in its first weeks.",
        "Seed is the budget-friendly route but needs time to fill in. Sod costs more and looks finished the day it goes down. We'll walk you through both options and handle the work either way."],
  included=["Core aeration","Overseeding and top dressing","Grass seeding","Sod installation","Soil prep and grading for new lawns","Patching bare or damaged areas","Aftercare guidance for your new grass"],
  sections=[
   ("Why aerate?", ["Two things hold most lawns back: compacted soil and a thick layer of thatch. Core aeration pulls small plugs of soil out of the lawn, opening space for air, water, and roots and breaking up both problems.",
                    "The plugs left on the surface dissolve back into the lawn within a week or two, which helps keep thatch in check. Aeration pays off most as a yearly habit rather than a one-time fix."],
    ["Better drainage after heavy rain","Air, water, and nutrients reach the roots","Looser, less compacted soil","New root and shoot growth","Less thatch build-up","Roots reach water more easily in dry spells","An ideal seedbed for overseeding","Fertilizer that actually reaches the roots"],
    "Fall is the top choice for aeration, with spring as a second option. Once a year is a good rule of thumb for most lawns."),
   ("Why overseed?", ["Overseeding puts new grass where old grass has thinned out. Combined with aeration and a light top dressing, it helps a lawn come back thicker and greener.",
                      "Right after aeration is the best moment to seed, since seed settles into the open holes and loosened soil. The pairing is an affordable way to revive a lawn worn down by a wet spring or a dry summer, and doing both in early fall gives new grass time to root before winter."], None, None),
  ],
  aftercare=[("Leave the plugs","Don't rake them up. They break apart on their own and fall back into the holes, often helped along by your mower within two to three weeks."),
             ("Keep the surface damp","Water right after seeding, then keep the top of the soil damp, not soggy, for about three weeks. After that, water more deeply but less often, ideally early in the morning."),
             ("Stay off it","Keep people and pets off seeded areas for the first few weeks so young seedlings aren't crushed."),
             ("First mowing","Wait until new grass is about 4 inches tall. Use a sharp blade, cut no more than a third of the height at a time, and leave the clippings."),
             ("Leaves on new grass","Raking can tear out young seedlings. Blow leaves off lightly or mulch them with the mower instead.")],
  photos=[None, None, None],
  tip=("Best window","Early fall is usually the best time to aerate and overseed in Southeastern PA, giving new grass time to root before winter."),
  related=["mowing","property-maintenance","yard-clean-up"]),
 dict(slug="yard-clean-up", name="Yard Clean-Up", icon="cleanup", season="Spring · Fall",
  card="Weeds out, leaves raked, and beds tidy before the next season.",
  promise="Reset your yard: weeds pulled, leaves raked, and beds tidied before the next season.",
  desc=["Take proactive steps to ensure your lawn's vitality and beauty for the upcoming year. By removing weeds, raking fall leaves, and maintaining garden beds, you can prevent debris buildup throughout the season and into winter."],
  included=["Weed removal","Raking leaves","Garden bed clean-out and upkeep","Debris hauled away"],
  photos=["berger-beds-11","berger-beds-17","berger-beds-13"],
  tip=("Before winter","Clearing leaves and debris before winter helps prevent mold, fungus, and pests, and protects the lawn through the cold months."),
  related=["leaf-removal","trimming","property-maintenance"]),
 dict(slug="leaf-removal", name="Leaf Removal", icon="leaf", season="Fall",
  card="Leaves raked and hauled away before they smother the lawn.",
  promise="Leaves raked and removed from your property before they trap moisture and invite mold and pests.",
  desc=["Leaving leaves to accumulate on your lawn can trap moisture, creating a breeding ground for damaging fungus and mold growth. Accumulated leaves can also provide a breeding ground for pests and insects.",
        "We will rake and remove leaves from your property, reducing these risks and maintaining the health and beauty of your lawn."],
  included=["Raking leaves from the lawn","Clearing beds, walkways, and edges","Leaves removed from your property","One-time or repeat visits"],
  photos=["berger-seasonal-03","berger-seasonal-01","berger-seasonal-02"],
  tip=("Timing","Book once most leaves have dropped. Heavy leaf years may need a follow-up visit."),
  related=["yard-clean-up","mowing","snow-services"]),
 dict(slug="trimming", name="Trimming", icon="trimming", season=None,
  card="Trees and shrubs trimmed for looks, plant health, and safety.",
  promise="Healthier trees and shrubs, a safer property, and a sharper look.",
  desc=["Trimming trees and bushes serves a dual purpose: it enhances the visual appeal and aesthetic charm of your landscape while also bolstering the health of your trees and promoting safety on your property.",
        "Our services extend to the removal of plants and shrubbery to meet your landscaping needs comprehensively."],
  included=["Tree and bush trimming","Hedge shaping to the height and form you want","Plant and shrub removal","Clean-up and haul-away of trimmings"],
  photos=["berger-trimming-01","berger-trimming-02","berger-trimming-s228"],
  tip=("Right time, right plant","The best time to trim varies by plant. We'll recommend timing that won't hurt flowering or growth."),
  related=["tree-planting","yard-clean-up","property-maintenance"]),
 dict(slug="tree-planting", name="Tree Planting", icon="tree", season="Spring · Fall", draft=True,
  card="Shade trees, ornamentals, and evergreen screens, planted with clean mulch rings.",
  promise="New trees and evergreen screens, planted and finished with a clean mulch ring.",
  desc=["New trees add shade, privacy, and structure to a property for years to come. We plant shade and ornamental trees and evergreens, then finish each one with a clean mulch ring that holds moisture and keeps mowers and trimmers away from the trunk.",
        "From a single specimen tree by the front walk to a row of evergreens along a fence line for privacy, we'll talk through placement with you before we dig, including how large each tree will grow."],
  included=["Planting shade trees, ornamental trees, and evergreens","Mulch rings around each new tree","Evergreen rows for privacy along fences and property lines","Decorative stone ring borders where you want them","Ongoing care through Property Maintenance"],
  photos=["berger-trees-s592","berger-cleanup-s610","berger-trees-s590","berger-trees-s237","berger-cleanup-s609","berger-trimming-s354"],
  tip=("Planting season","Spring and fall are generally the best times to plant in Pennsylvania. Give new trees regular, deep watering through their first season."),
  related=["trimming","custom-landscaping","property-maintenance"]),
 dict(slug="junk-removal", name="Junk Removal", icon="junk", season=None,
  card="One item or a full garage. We lift, haul, recycle, and donate.",
  promise="From a single old appliance to a full garage clean-out, we do the heavy lifting.",
  desc=["At Berger Landscaping LLC, we offer a hassle-free junk removal service to help you declutter your space. Our friendly team can take care of everything from old furniture and yard debris to appliances and household clutter.",
        "We are committed to eco-friendly practices, ensuring that items are recycled or donated whenever possible, reducing waste and benefiting the community. Whether it's a single item or a full garage cleanout, we make the process easy and stress-free.",
        "Trust us to do the heavy lifting, so you can enjoy your clean and organized space! We can also provide references to professional cleaning and organizing companies."],
  included=["Old furniture, appliances, and household clutter","Yard debris, brush, and branches","Single items through full garage clean-outs","Items recycled or donated whenever possible","References to cleaning and organizing companies"],
  photos=["berger-crew-01", None, None],
  tip=("Faster quotes","Photos or a short description of what you need removed help us quote it."),
  related=["yard-clean-up","property-maintenance","trimming"]),
 dict(slug="snow-services", name="Snow Services", icon="snow", season="Winter",
  card="Plowing, removal, and salting for driveways and commercial lots.",
  promise="Plowing, snow removal, and salting to keep driveways and lots safe.",
  desc=["At Berger Landscaping LLC, we prioritize keeping your property safe in winter. Our snow plowing and removal services efficiently clear snow from driveways and commercial lots, ensuring safe surfaces.",
        "We also offer salting services to reduce slips and falls using effective salt treatments. Ask about our pet-safe ice-melt options that protect your pets while ensuring traction for walkways."],
  included=["Snow plowing for driveways and commercial lots","Snow removal","Salting to reduce slips and falls","Pet-safe ice-melt options (ask us)"],
  photos=["berger-snow-01", None, None],
  tip=("Early openers","If your business opens early, ask us about plow timing when you sign up."),
  related=["junk-removal","property-maintenance","leaf-removal"]),
]
SVC = {s["slug"]: s for s in SERVICES}
# map FAQ group names -> slug
FAQ_KEY = {"Mowing":"mowing","Property Maintenance":"property-maintenance","Custom Landscaping Solutions":"custom-landscaping",
           "Yard Clean-Up":"yard-clean-up","Leaf Removal":"leaf-removal","Trimming":"trimming","Tree Planting":"tree-planting","Aeration, Sod & Seeding":"aeration-sod-seeding","Junk Removal":"junk-removal","Snow Services":"snow-services"}
for g, items in FAQS.items():
    SVC[FAQ_KEY[g]]["faqs"] = items

SEASONS = {
 "spring": dict(label="Spring", note="Beds, mulch, and the first cuts of the year.", items=[("yard-clean-up","Clear winter debris and get beds ready for growth."),("property-maintenance","Mulch installation and bed upkeep for the season ahead."),("mowing","Get on the schedule before the grass takes off.")]),
 "summer": dict(label="Summer", note="Steady cuts and sharp edges through the heat.", items=[("mowing","Weekly cuts at the right height to handle summer heat."),("trimming","Shape hedges and cut back branches near walks and roofs."),("custom-landscaping","Plan a new bed, path, or redesign with Drew.")]),
 "fall": dict(label="Fall", note="Leaves off the lawn before winter sets in.", items=[("leaf-removal","Rake and haul leaves before they smother the grass."),("yard-clean-up","Fall clean-up to prevent mold, fungus, and pests."),("trimming","Cut back shrubs and plants as the season ends.")]),
 "winter": dict(label="Winter", note="Safe drives, walks, and lots after every storm.", items=[("snow-services","Plowing, removal, and salting for drives and lots."),("snow-services#pet-safe","Ask about pet-safe ice-melt options."),("junk-removal","Indoor season: clear out the garage or basement.")]),
}

REVIEWS = [
 dict(name="Nancy LaPella", meta="16 reviews · 1 photo", text="Highly recommend Berger - their team is respectful, efficient, knowledgeable, fairly priced and overall they did a fantastic job for us.", reply="Thank you so much for the kind words, it is a pleasure working for you!"),
 dict(name="Christina Erbicella", meta="Local Guide · 17 reviews · 6 photos", text="Drew and his team did an amazing job with our landscaping. Highly recommend.", reply="Thank you so much! Looking forward to future jobs for you!"),
 dict(name="Ashley D", meta="Local Guide · 21 reviews · 6 photos", text="The team has been cutting my yard this year all so far and doing a wonderful job keeping my grass maintained. We hate cutting our grass with our very large hill in our yard and it has looked nothing short of amazing all year. Thanks! We are very happy.", reply=None),
 dict(name="Cindy Homol", meta="6 reviews", text="Drew and his crew are a pleasure to work with, knowledgeable, and dependable.", reply=None),
]

CATS = [("lawn","Lawns & mowing"),("beds","Beds & mulch"),("hardscape","Stonework & patios"),("trimming","Trimming & shrubs"),("trees","Trees"),("seasonal","Fall work"),("snow","Snow"),("crew","Crew & equipment")]

ALT_FIX = {
 "berger-hardscape-01":"Timber-framed gravel steps edged with river rock on a hillside",
 "berger-hardscape-02":"Raised paver patio with a block retaining wall and bistro table",
 "berger-hardscape-10":"Paver walkway beside a garage with fresh mulch",
 "berger-crew-03":"Crew member carrying a flat stone through a bed being rebuilt",
 "berger-snow-01":"Pickup truck with a red plow on a snow-covered road",
 "berger-seasonal-03":"Crew raking fall leaves into a dump truck",
 "berger-crew-01":"Crew unloading a dump trailer at a wooded job site",
}
