import os
import re

csv_data = {
    "234-washington-ave": "1 Private showing last Monday. Overall went well. Pending more detailed feedback from the agent. Will continue to follow up",
    "763-pennsylvania-avenue-unit-116": "We had one private showing. The buyer is an investor who is already very familiar with both the building and the area. The agent mentioned that the client is currently running numbers and evaluating the opportunity before making any decisions.",
    "1376-sw-4th-st-7": "We had one showing this week, and overall the feedback was positive. The buyer is originally from Miami and currently lives in DC. She seemed to really like the home and mentioned wanting to schedule a second showing so her husband can see the garage, as he wasn’t able to attend the first visit.",
    "7334-harding-unit-6": "We had 3 private showings total — two for rent and one for sale. For the rental showings, one client decided to move forward with another option that was more affordable. The second rental showing went well overall, but the client is still exploring other options before making a decision. For the sale showings, one buyer mentioned they did not like the building itself and will not be moving forward. There was one other showing cancelled last minute, but we are currently working on getting it rescheduled.",
    "6061-collins-avenue-unit-5f": "The first buyer is a single man relocating from Denver, although he’s originally from Miami. He’s looking for a beachfront condo to use as a home base while also renting it out when he’s out of town seasonally, so he really liked the building’s flexible rental policies. The views and location were the biggest selling points for him. His agent mentioned the unit is currently a top contender, although they are still exploring other options. Sunday’s showing was with investor clients from Ohio who already own several units at the Fontainebleau. They also responded very positively to the unit and intend to use it as a rental property. Their main hesitation was the timeline for the work that still needs to be completed.",
    "17301-biscayne-boulevard-unit-1401": "The first showing was with agents who FaceTimed their client in Brazil during the walkthrough. They were already familiar with the building and mentioned their client liked the unit. Their client is expected to be in town in early June and would like to see it in person if it’s still available at that time. The second showing was with a couple who were both the Realtors and the clients themselves. They recently moved from California and are currently renting in Mid-Beach while looking for a place to put down roots. They are primarily searching closer to the beach, but were drawn to this unit because of the views. They also liked the updated features throughout both the unit and the building. At the moment, they are still exploring their options before making a decision.",
    "1945-s-ocean-dr-unit-m2": "We had two private showings. One of the buyers visited the unit for a third time and appears to have strong interest. He mentioned that if he decides to submit an offer, it will likely be an aggressive one. The second showing ultimately decided against the unit because it is on the ground floor. The prospective tenant was a young female and had concerns regarding safety.",
    "244-biscayne-3702": "The buyer is not interested.  The wife had a look around the neighborhood and didn’t like the neighborhood.",
    "8000-harding-avenue-unit-2b": "We had one private showing on Monday afternoon. The buyer is a father looking to purchase the unit for his daughter. They liked the layout of the unit as well as the location, but are still touring other properties before making a decision. There was also another showing request, but unfortunately it could not be accommodated due to the tenants not being available for the requested time change.",
    "88-sw-7-st-1012": "We had two private showings. The first buyers are still considering whether or not they will move forward with submitting an offer - they liked it. The second showing decided not to move forward, as they did not feel the area was the right fit for them.",
}

properties = [
    "10449-sw-78th-st",
    "1376-sw-4th-st-7",
    "1710-nw-106-terr",
    "17301-biscayne-boulevard-unit-1401",
    "1945-s-ocean-dr-unit-m2",
    "234-washington-ave",
    "244-biscayne-3702",
    "320-85-st-15",
    "6061-collins-avenue-unit-5f",
    "7334-harding-unit-6",
    "763-pennsylvania-avenue-unit-116",
    "8000-harding-avenue-unit-2b",
    "88-sw-7-st-1012"
]

base_dir = r"C:\Users\Daniel Estrada\.gemini\antigravity\scratch\weekly-showing-reports\agents\joanna-jimenez"

for prop in properties:
    file_path = os.path.join(base_dir, prop, "index.html")
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Update Social Media Views
    social_views = "716" if prop == "88-sw-7-st-1012" else "272"
    # Find the social media views row
    # <div class="metric-name">Social Media Views</div>
    # <div class="last-7">+...</div>
    html = re.sub(
        r'(<div class="metric-name">Social Media Views</div>\s*<div class="last-7">\+)[\d,]+(</div>)',
        f'\\g<1>{social_views}\\2',
        html
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

print("Updated properties.")
