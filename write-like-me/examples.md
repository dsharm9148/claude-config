# Diya's Writing Samples

A corpus of real writing across contexts: Slack, email, analysis docs, essays, research writing. Match the **closest context** before drafting.

---

## Example 1: Personal intro / "about me" blurb

**Context:** short personal bio used on a personal site, when asked "tell me about yourself", or as the top of a cover letter
**Text:**
> I'm a rising fourth-year at Georgia Tech studying Computer Science, with concentrations in Artificial Intelligence and Human-Computer Interaction. I'm also pursuing a Biology minor and a Global Engagement certificate.
>
> I'm especially interested in work at the intersection of technology and health. Most recently, I was an Applied Machine Learning co-op on the Women's Health team at WHOOP, where I worked with large-scale health data and got to build more user-facing, production-level tools and features. Before that, I did applied ML research at Georgia Tech, worked in data science at the UMD Blanpied Lab on synaptic imaging research, and completed a mechanical engineering internship at the Johns Hopkins University Applied Physics Laboratory designing an electronic sensor for mass casualty response scenarios.
>
> Outside of work and school, I love anything sports and outdoors, from surfing to skydiving. Through my Global Engagement certificate, I've had the chance to study and travel across multiple continents, which inspired much of the photography featured on this site.

---

## Example 2: Analysis / results document (technical writeup)

**Context:** internal Confluence-style doc summarizing an analysis with a recommendation; opens with an exec summary, then methodology, then numbers, then proposed threshold, then next steps
**Text:**
> **Executive Summary**
>
> The ovulation detection pipeline takes a per-night sleep window (a start time and an end time) from an upstream sleep detection algorithm (SAD). We want to know how much the accuracy of the downstream Bloom ovulation detection model changes if those two times are shifted, and use that to set a tolerance for evaluating new sleep detection algorithm candidates (i.e. SAND).
>
> We re-ran the full pipeline on 105 users (216 cycles) for 152 different combinations of (start_shift, end_shift), in 0.5-hour steps, covering shifts up to ±9 hours on the start time and ±12 hours on the end time. For each combination we recorded:
> - MAE: Average number of days between the predicted and true ovulation date for:
>   - Prospective Algorithm: makes an ovulation prediction at the start of each cycle using previous temperature and menstrual cycle patterns
>   - Confirming Algorithm: refines the original prediction by monitoring nightly skin temperature for a rise indicating that ovulation has occurred
> - Detection Rate: Percentage of cycles where the confirming algorithm successfully detected a temperature rise and produced a prediction
> - Phase separation ratio (PSR): used to quantify how well skin temperature measurements distinguish between menstrual cycle phases
>
> The four single-direction shifts are not symmetric. Moving the sleep start earlier or the sleep end later has very little effect while moving the sleep start later or sleep end earlier and especially doing both has the biggest effect. The reason for this asymmetry is likely because the skin-temp signal that the ovulation model relies on (max and 90th percentile) sits in the early part of the sleep window. Additionally, the low-motion filter built into our pipeline discards skin-temp readings outside true sleep. Padding the reported window with extra time on either side gets filtered out before it reaches the model. However, trimming the window (especially trimming the early portion) removes the part of the signal the model actually uses.
>
> **Proposed threshold:** At 3.5 h on each side, confirming MAE is 1.97 d (95% CI 1.72–2.22), inside the 2.5 d regulatory bound with about 0.28 d of margin on the upper CI. At 4 h on each side it is 2.29 d (95% CI 2.01–2.63), crossing the bound. No threshold is needed on the other two directions (sleep start earlier, sleep end later).
>
> **Next steps proposal:** For each candidate sleep algorithm, run a test that computes the per-night change in sleep start and sleep end relative to the current model, and reports the upper bound of the 95% CI of that change in each direction. Gate the candidate on whether that upper bound falls within ~3.5 hours. A candidate model whose combined trim stays under 3.5 h on each side is expected to keep confirming MAE inside the 2.5 d regulatory bound.

---

## Example 3: Cold outreach email (to a company)

**Context:** reaching out to a company she admires while she's in town for a co-op, asking to visit and connect
**Text:**
> Hi Cognito Therapeutics Team,
>
> My name is Diya Sharma, and I'm currently an Applied Machine Learning Science Co-op at WHOOP here in Boston. I'm also a third-year student at Georgia Tech studying Computer Science and Neuroscience.
>
> I recently came across Cognito's work in non-invasive neuromodulation for neurodegenerative diseases and found it incredibly exciting. The intersection of neuroscience, hardware, and machine learning is especially interesting to me.
>
> Since I'm based in Boston for my co-op, I'd love to take advantage of being nearby and was wondering if it might be possible to visit sometime, even just briefly, to meet someone on the team, learn more about what you're building, and potentially get a tour. I'd really value the chance to hear more about your approach and the problems you're tackling.
>
> I know schedules can be busy, but if there's any opportunity to connect, I'd be happy to work around what's convenient for you.
>
> Thanks so much, and I hope to connect soon!
>
> Best,
> Diya Sharma

---

## Example 4: Slack to team (sharing a useful tool / process)

**Context:** following up on a working session by sharing a tool and a recommended workflow with the team
**Text:**
> Hey all! Following our discussion in the Bloom working session, I'm sharing a helpful Claude Code tool for reviewing AI-generated code: `/simplify`
>
> This skill helps clean up code by checking the diff in your branch and then launching 3 agents in parallel:
> - **Reuse**: searches the codebase for existing utilities that could replace newly written code.
> - **Quality**: flags bad patterns: redundant state, copy-paste blocks, unnecessary comments that explain what instead of why, and nested conditionals 3+ levels deep.
> - **Efficiency**: looks for wasted work: redundant computations, N+1 patterns, missed parallelism, reading entire files when only part is needed, etc.
>
> Here is what I would recommended before opening a PR:
> 1. Build/code with AI
> 2. Run `/simplify`
> 3. Review the suggested cleanup/refactors
> 4. Validate tests + behavior
> 5. Do a final manual diff review before requesting reviews
>
> This is a general skill and doesn't use repo specific standards, so it's still important to manually review.
>
> Based on this article here, you can also pair this with `/batch`:
> - Before running simplify you can run `/batch` to identify similar complexity patterns across the codebase
> - Or you can apply consistent cleanup/refactors across multiple files after using `/simplify` on one implementation

---

## Example 5: Analysis recommendation with threshold rationale

**Context:** writing up a follow-on analysis to inform a product/eng decision, with a clear recommended threshold and the reasoning behind it
**Text:**
> When using the actual cycle length instead of Bloom's predicted cycle length mean, the confirmed ovulation estimate shifts by ~1.25 days on average. A small subset of cycles exhibit larger discrepancies: ~5% shift by more than 3 days, and ~3% shift by more than 4 days. These outliers are concentrated among users with abnormal cycle regularity (>7 days of variation).
>
> Based on these results, we recommend using a gap threshold of 3 days between the old confirmed ovulation and the updated MCI estimate to decide when to invalidate a previously confirmed ovulation.
>
> The case for a 3-day threshold is well-supported by the analysis. It sits at the P90 of the confirming gap distribution, meaning 90% of cycles naturally fall below it. This threshold would flag ~5% of cycles for invalidation, concentrated among users with irregular cycles, where Bloom's prospective prediction is most likely to diverge from reality.
>
> **Background**
>
> When a past cycle is edited, MCI updates both the cycle boundaries and the ovulation estimate. However, temperature-based confirmed ovulations (Bloom predictions) are designed to persist unless they become inconsistent with the updated cycle.
>
> This raises a key question: when should a previously confirmed ovulation be invalidated?
>
> One approach under consideration is to compare:
> - The original confirmed ovulation (based on Bloom's prospective estimate + temperature), and
> - The ovulation estimate from MCI (based on the actual cycle length)
>
> If the gap between these two estimates is sufficiently large, the original confirmation may no longer be reliable. In those cases, we could invalidate the confirmed ovulation and fall back to MCI-based ovulation phase estimates.
>
> We are still evaluating whether this is the right approach. This analysis is intended to inform that decision by helping us understand:
> - How often large discrepancies arise between Bloom and MCI ovulation estimates
> - How those discrepancies impact the accuracy of confirmed ovulation
> - The potential downstream effect on user perception when a previously confirmed ovulation is changed or removed

---

## Example 6: Meeting notes / analysis summary

**Context:** structured notes capturing a decision under consideration plus the numerical results that bear on it
**Text:**
> One approach under consideration is to compare:
> - The original confirmed ovulation (based on Bloom's prospective estimate + temperature)
> - The ovulation estimate from MCI (based on the actual cycle length)
>
> If the gap between these two estimates is sufficiently large, the original confirmation may no longer be reliable. In those cases, we could invalidate the confirmed ovulation and fall back to MCI-based ovulation phase estimates.
>
> **Analysis Results**
> - Bloom MAE vs ground truth = 1.6
> - MCI MAE vs ground truth = 1.4
> - ~30% of predictions do not change
> - ~6% of predictions shift by more than 3 days, and ~3% shift by more than 4 days.
> - These outliers are concentrated among users with abnormal cycle regularity (>7 days of variation).
>
> With no edits (delta = 0), prospective Bloom and MCI disagree by 1.79 days, with only 18% cycles matching. For confirming, Bloom and MCI disagree by 1.25 days MAE, with only 30% of cycles matching exactly.
>
> Disagreement grows roughly linearly as edits increase in either direction (MAEs are for the confirming model):
>
> Negative edits (shorter cycles):
> - -1 day → 1.30 days MAE
> - -2 days → 1.49 days MAE
> - -3 days → 1.75 days MAE
> - -5 days → 2.36 days MAE
> - -10 days → 4.15 days MAE
>
> Positive edits (longer cycles):
> - +1 day → 1.36 days MAE
> - +2 days → 1.74 days MAE
> - +3 days → 2.26 days MAE
> - +5 days → 3.76 days MAE
> - +10 days → 8.50 days MAE
>
> Once edits reach ±3 days, Bloom's ovulation predictions can differ by an MAE of more than 2 days from MCI, and at ±5 days the disagreement approaches ~4 days. Therefore, we should be cautious about showing Bloom predictions when the user edits their cycle by 3 or more days.

---

## Example 7: Short administrative email

**Context:** brief request to an institutional contact to retrieve a document
**Text:**
> Hello,
>
> I hope you're doing well. I took the BACE exam back in high school through the ARL Biotechnology program, and I need to download a copy of my BACE certificate. Could you please let me know how I can access or retrieve it?
>
> Thank you for your time and assistance.
>
> Best,
> Diya Sharma

---

## Example 8: Email to a research PI / mentor

**Context:** following up with a former research mentor on plans, after a delay; warm but efficient
**Text:**
> Hi Dr. Blanpied,
>
> The semester's been busy but going well! Apologies for the delayed response; we're currently on spring break, and I just got around to catching up on emails. May 6th still works for my schedule!
>
> Regarding upcoming work, I couldn't locate the grant you mentioned, but I did take a look at the Ament lab's website and their publications. I've had very little experience with transcriptomics (I only did one project in high school), but I'm open to exploring that avenue!
>
> Additionally, I think a collaboration with the Losert lab would be very useful in terms of methods, as you suggested, and also for the boot camp, which would be a great starting point. I saw that they have some interesting applications of both AI and computer vision algorithms, so collaborating with them seems like an exciting opportunity!
>
> Best,
> Diya

---

## Example 9: Email to a former professor

**Context:** keeping in touch after they wrote a recommendation; share good news and a personal question
**Text:**
> Hi Professor Henneman,
>
> I hope you've been doing well! I wanted to follow up and let you know that I was accepted into the BSMS program! Thank you again for writing such a strong recommendation. I really appreciate your support.
>
> I also wanted to say that I really enjoyed last summer's class as well. It was one of the most memorable classes I've taken at Tech, and I learned a lot from it.
>
> I hope you have a great summer coming up! Any interesting plans, travel, or projects ahead?
>
> Best,
> Diya

---

## Example 10: Concise field notes / lab notebook

**Context:** dated, structured observation entries for a research lab notebook; describe what was seen plus what it implies
**Text:**
> **Week of 2/2 Lab Notebook**
>
> *Field Observations 02/03/2025 5:30 pm*: Went down to the river area behind the business school. Observed a couple of seagulls bathing in the water, making little to no noise. There were around twenty gulls sitting on the median just resting. A few new gulls flew into the area making constant squawks until they landed on the same median. From all observations, it seems like it is common behavior to announce when you are landing.
>
> *Field Observations 02/03/2025 5:45 pm*: In the same area as the previous observation. There was a different bird sitting on the same median. A seagull came in and started diving/swooping at the bird. While it did this, it made an aggressive, high-pitched scream. This set off another interaction between about three gulls next to the other bird. They put their heads down and into their bodies and made the same screaming type of noise. All of these are social behaviors.
>
> *Field Observations 02/03/2025 9:15 pm*: Right outside of the UniCol cafeteria, there were around ten to fifteen seagulls flying and making constant noise. The sounds were primarily short squawks but at a high frequency. This behavior fits under flying. This has been a pattern we have noticed most nights.
>
> *Class Discussion 02/04/2025 10:30 am*: Discussed a paper about how man-made armoring affects beach vegetation. Although the topic of this paper doesn't relate to our research, we can still use it as a blueprint to write our final paper. We learned from this paper what we've learned from the others, which is that it is necessary to clearly explain how you analyzed your data and the specific parameters you used even if you think your paper is only for experts in your field. However, the actual sections of this paper were very well written so we will follow these for how to write our paper, although it will be shortened.
>
> *Field Observations 02/05/2025 12:30 pm*: Observed multiple seagulls in the courtyard near the library. There seems to be people feeding them but at the time of the recording, they weren't actively being fed. The main behavior here was wandering and constant chirping as if they were in search of a human with food. In this case, the seagulls avoided each other and kept their distance but were equally as loud as each other.

---

## Example 11: Resume bullets

**Context:** action-verb-led bullets describing past roles; one line each; quantified where possible
**Text:**
> **WHOOP, Applied Machine Learning Science Co-op (Boston, MA, Jan 2026 – Present)**
> - Currently working on data science initiatives for a SaMD QMS-regulated Class I medical device, adhering to FDA standards
> - Leveraging Snowflake and EzDeploy to query, validate, and analyze large-scale physiological and product data
> - Conducting a comparative analysis of internal data pipelines to evaluate performance and downstream analytical impact
>
> **UMD School of Medicine, Blanpied Lab, Data Science Intern (Baltimore, MD, Summer 2024, Oct 2022 – Apr 2023)**
> - Developed a classification system (SVM, Random Forest, Gradient Boosting) to automatically differentiate synapses
> - Applied feature engineering and dimensionality reduction techniques using SciKit-Learn and OpenAI
> - Automated data collection and image processing pipelines using a combination of Java, MATLAB, and Python
>
> **Johns Hopkins University Applied Physics Laboratory, Mechanical Engineering Intern (Laurel, MD, Jun 2022 – Mar 2023)**
> - Thought of project idea for a fully electronic triage tagging system, leading to acquisition of a $20,000 grant
> - Led a three-person intern team in the design and development of a novel medical sensor component for the project
> - Presented research and sensor prototype at the 2023 IEEE Integrated STEM Education Conference

---

## Example 12: Masters application essay (narrative)

**Context:** personal essay opening with a concrete scene, threading a theme, returning to the scene as a frame
**Text:**
> I hopped on the metro to WHOOP's Boston office, rode the elevator to the eighth floor, and peeked out at Fenway Park, covered in snow. I had a cup of hot chocolate as a little comfort before my meeting with a Senior AI Engineer. I was only a few weeks into my co-op, still getting used to the rhythm, but I wasn't going to miss out on the coffee chats. At WHOOP, you can meet up with anyone for coffee, on the company, just to connect.
>
> I always ask people about their education, so of course I had the engineer tell me why he went for a master's in AI and machine learning. Grad school, he said, gave him more than just technical skills or a higher salary later on. It also let him really dig into the systems he was building. Not just the "how," but the "why." He talked about his research, how it sharpened his interests, and eventually pulled him into large language models and leading WHOOP's AI coach project. For him, grad school wasn't just a box to check. It opened up a deeper understanding and new directions in AI he hadn't even thought about before.
>
> Later, I caught up with my manager, a clinical data scientist with a master's degree too. He had told me grad school helped him explore the overlap between data science and healthcare before deciding where he wanted to go. I started to notice a trend. Most of the people I admire at work used graduate study to deepen their skills and broaden their view.
>
> I've seen this play out in my own life during my undergrad research. Through Georgia Tech's VIP program, I worked on wearable devices and used AI to analyze biosignal data. I only joined that VIP to satisfy my junior capstone, but that project got me hooked on wearable tech and is the whole reason I ended up at WHOOP. What started out as just curiosity turned into real hands-on work, applying machine learning to physiological data and getting a taste of the wearable device industry.
>
> Honestly, every research or academic experience I've had has nudged me in a new direction. Right now, I'm excited about health tech and AI-powered products, but I know this field moves fast. A graduate program gives me the chance to dig deeper into machine AI, learn more about where the field might be heading, and get involved in research that could take me somewhere completely unexpected. More than anything, a master's feels like a chance for focused exploration. Just like research led me to wearable AI, I know grad school could guide me to the next big innovation.

---

## Example 13: "Why this school" essay (themed structure)

**Context:** essay built around a memorable refrain ("the three A's"), grounding each section in a concrete personal anecdote
**Text:**
> I always wrap up my campus tours in front of Tech Tower, wearing my blue "GT Tour Guide" polo, looking out at a group of prospective students. I tell them exactly why I picked Georgia Tech for undergrad. I call it the three A's: Academics, Athletics, and Atlanta. Every time I say it, I realize that those same three reasons are why I want to pursue my graduate education here.
>
> Starting from academics, Georgia Tech's endless opportunities blew me away. The classes here don't just make you work hard but they force you to think deeper, code smarter, and question how you build things. For grad school, I'm especially excited to take CSE 6250 Big Data for Health and CS 6220 Big Data Systems & Analysis to build my skillsets with data analytics. I'm also looking forward to returning to the Bio-Interfaced Translational Nanoengineering Group that I did my VIP through as a graduate student. I hope to pursue the insomnia detection research I was previously working on. I've seen that Tech has a culture where people truly work together and a program that doesn't just teach you basics but that pushes you to get hands-on experience working in the field.
>
> As a sports writer and photographer for The Technique, Tech athletics have become a huge part of my life. Most weekends, I find myself on the sidelines at Bobby Dodd or courtside at McCamish with a camera in hand. Covering everything from big games to intramurals has introduced me to people all over campus, and it's taught me more about leadership and storytelling than I ever expected. I can't picture grad school without that creative balance and sense of community. I want to keep working with The Technique and maybe even run for president as a grad student.
>
> Moving to Atlanta was nerve wracking, and I'd never lived in the heart of a major city before. But I quickly fell in love fast with the way Tech feels like its own little world, but is right in the heart of everything Atlanta has to offer. Grand Challenges events, Braves games, nights at the Fox Theatre, afternoons at the aquarium, even SCPC night at Six Flags all made Atlanta feel like home. As a grad student, I want to keep giving back. I'll likely join Grand Challenges as a facilitator or teaching assistant, continuing to help others settle in and find their place just like I did.
>
> Grad school's a big leap, and I want to take it somewhere I already know supports me and pushes me to grow. Georgia Tech's given me the foundation, the chances, and the confidence to go after more. I'm ready to keep building on that right here.

---

## Example 14: Career goals statement (short)

**Context:** a few sentences on post-degree plans for an application
**Text:**
> After earning this degree, I envision beginning my career in machine learning engineering or data science, ideally within the wearable technology field. I want to build AI systems that turn complicated physiological or behavioral data into real, useful insights for people. Down the road, I see myself stepping up as a technical lead or moving into a senior role, connecting big ideas with actual products and helping teams create AI that's both responsible and scalable. In the end, I want to play a part in developing tech that makes a difference in people's health.

---

## Example 15: Research paper abstract

**Context:** formal academic abstract with hypothesis → method → results → significance; dense, passive-tolerant, defined acronyms
**Text:**
> Excitatory and inhibitory neurons possess different synaptic structures and molecular characteristics, due to their distinct roles in neural circuitry. Additionally, there exist various subtypes of interneurons with well-defined functional differences. However, it remains unclear whether these functional differences are manifested in the molecular organization of protein clusters at excitatory synapses onto these interneurons. We combine confocal microscopy, quantitative image analysis, and machine learning to investigate synaptic protein cluster organization at different synapse types, focusing on Munc13 and PSD-95 protein clusters at excitatory-to-inhibitory (Ex→Inh) and excitatory-to-excitatory (Ex→Ex) synapses. Furthermore, we employ five neuropeptide markers (PV, SST, CCK, NPY, and VIP) to identify and differentiate subtypes within Ex→Inh synapses, aiming to elucidate finer distinctions in synaptic organization. Our findings reveal larger and denser Munc13 clusters at Ex→Inh synapses compared to Ex→Ex synapses, indicated by a significant increase in cluster area and intensity. Among Ex→Inh synapse subtypes, there are notable differences in the ratios of Munc13 and PSD-95 intensities in certain cases, while in others, these ratios are similar, implying comparable cluster organization among those subtypes. Through dimensionality reduction and clustering techniques, we reveal a continuous spectrum of variation among synapse classes, underscoring the presence of both distinct and shared characteristics across synapse subtypes. These variations play a crucial role in synaptic transmission and correspond to the functional differences among different neuron types. Identifying the correlation between protein organization and synapse subtype establishes a foundation for future experiments aimed at understanding nanocluster organization and trans-synaptic alignment at such synapse types.
>
> **Keywords:** Munc13, PSD-95, excitatory synapses, inhibitory subtypes, synapse organization, synapse types, fluorescence imaging, unsupervised machine learning

---

## Example 16: Research poster prose

**Context:** poster-style sections with formal section headers (Importance, Goal, Hypothesis, Methods, Results, Discussion); each section is 1–2 tight paragraphs
**Text:**
> **Importance of Synaptic Protein Clusters**
>
> Neurocognitive diseases, such as autism spectrum disorder, are associated with an irregular organization of key protein clusters at synapses. Postsynaptic density-95 (PSD-95) is a cluster-forming scaffolding protein that anchors neurotransmitter receptors in the postsynaptic density. Abnormal PSD-95 organization has been proven to underlie impaired cognition and intellectual disability. Mammalian uncoordinated-18 (Munc13) is another cluster-forming protein that is essential for neurotransmitter release in the presynaptic active zone.
>
> The size and intensity of both PSD-95 and Munc13 clusters are directly related to synaptic strength; however, the differences in organization across various synapse types is not well understood. Excitatory synapses containing these proteins are made onto both excitatory neurons, which promote neural activity, and inhibitory neurons, which prevent excessive activity. Therefore, researching the differences between protein clusters at excitatory synapses onto excitatory neurons (Ex→Ex) and at excitatory synapses onto inhibitory neurons (Ex→Inh) is crucial for understanding synaptic transmission and identifying abnormal synaptic behavior.
>
> **Hypothesis**
> - Munc13 is more dense at excitatory synapses onto parvalbumin-expressing (PV) neurons than at Ex→Ex synapses, as shown by prior research.
> - Different inhibitory neuron subtypes have unique roles in neuronal circuits, so the Munc13 organization at excitatory synapses onto different inhibitory neuron subtypes will vary.
>
> **Discussion and Conclusion**
>
> The area of Munc13 clusters is significantly greater in excitatory synapses onto three of the inhibitory neuron subtypes (Avg. 0.26 μm²) compared to Ex→Ex synapses (0.24 μm²). Similarly, Munc13 cluster intensity is on average 1.39 times greater in all Ex→Inh synapses compared to Ex→Ex synapses. PSD-95 clusters had little to no significance between neuron types.
>
> The results indicate larger and denser Munc13 clusters in Ex→Inh synapses compared to Ex→Ex synapses. The ratio of Munc13 to PSD-95 is also statistically different between inhibitory neuron subtypes, suggesting unique protein organization among those subtypes.
>
> Certain factors, such as the method for cell type selection, were not ideal due to a significant proportion of cells that express more than one marker. A Cre-driven mouse line would allow for cell-specific genetic expression and improved accuracy. Furthermore, variability among CCK neurons can be aided by increasing the sample size in future experiments.
>
> The correlation between Munc13 cluster area/intensity and synapse type establishes a foundation for future experiments that aim to understand protein organization at synapses. Such research could help identify molecular abnormalities related to synaptic protein clustering that are associated with neurocognitive diseases.

---

## Example 17: Slack analysis status update (longer-form to manager)

**Context:** sharing analysis outputs, summarizing what the numbers show, and proposing next steps
**Text:**
> I'm forwarding the outputs from the analysis so far at this link here! The plots are available under `run_grid -> cards`. I also updated PR 330 with the flow/plot/utils scripts, so that can be reviewed anytime!
>
> A notable update from the latest runs. For confirming, the start +4 / end -4 gives an upper CI of 2.620 and also the start +5 / end -5 condition gives an upper CI of 2.711, which confirms that we've now crossed the 2.5 threshold, so I don't think we need to continue expanding the maximum magnitude shift further unless we want to see when the 3.0 requirement for prospective is crossed.
>
> There is a pretty clear trend that adding hours to start has the biggest impact on mae which tracks with our previous findings that skin temp max/90th is found towards the beginning of the users sleep. Also shifts to end have less of an impact which tracks with our theory that the low motion filter is protecting us from skin-temp readings after a user wakes up.
>
> From here, my current thinking on next steps is:
> 1. If needed, add more plots to address any remaining open questions or edge cases from the current outputs.
> 2. Re-run the analysis with smaller intervals (0.5-hour and potentially 0.25-hour intervals) so we can localize where the crossover occurs around the 2.5 threshold.
> 3. Using the start +/- end = 0 define a start threshold, and using the start = 0, end +/- define an end threshold.
> 4. Each plot has a download option, so save the key ones and consolidate everything into a Confluence doc for easier viewing.
>
> Let me know what you think, and definitely give any feedback on the current graphs/data as well. Thanks Will!

---

## Example 18: Slack to manager: PR status + return-offer ask

**Context:** quick status update to manager that pivots into a personal ask about a return offer; mixes professionalism with a friendly aside
**Text:**
> Hi Will, I've made the changes to PR 330 and responded to the comment on PR 331. Quick question: are these scripts actually meant to be merged/live in the repo, or are the reviews mainly just for checking the analysis logic? Just trying to understand what the expected final state is (merged code vs. analysis living on a branch).
>
> I would really love a return offer! Haha but more importantly, I hope you'd feel comfortable putting in a good word for me when doing the evaluation form! I've really valued this experience and would be excited about the opportunity to come back, though I totally understand that a lot of it depends on role availability and headcount.

---

## Example 19: Slack quick sanity-check question to teammate

**Context:** one-line check-in to verify a number against an existing source
**Text:**
> Hey Tatiana! Quick question: is the MAE from the preliminary assessment results our most recent performance metric? I'm trying to sanity check the MAE I'm getting from my sleep bounds analysis against something.

---

## Example 20: Slack reaction / "aha" moment in working chat

**Context:** real-time response building on a teammate's idea, then floating a follow-up proposal
**Text:**
> Ohhh yeahh great theory! The motion filtering is protecting us from getting skin temp after they wake up.
>
> So maybe we should provide two separate thresholds? One for sleep end and a different (likely more conservative) one for sleep start.

---

## Example 22: Casual personal email (catch-up with friend/peer)

**Context:** replying to a friend who asked about recent plans; chatty, exclamation points, "haha", shares own news and asks back
**Text:**
> Yes, we actually did make it out to Revere Beach! It was such a perfect sunny day, although the water was still absolutely freezing. Almost as cold as New Zealand glacier water haha. Still totally worth it though.
>
> Your upcoming travel plans sound incredible. The Virgin Islands are definitely high on my list, so you'll have to tell me all about it when you're back. And Japan sounds amazing too. Where are you planning to go? After the Pacific program, Ryan, Joel, and I spent a little time in Tokyo and absolutely loved it. The energy there was unlike anywhere else I've been.
>
> I've got a few adventures lined up this summer as well! Natalie has an internship in LA, so I'm going to spend some time out there with her in July and explore more of the West Coast. After that, we're planning a week-long road trip back to Atlanta with lots of national park stops along the way, which I'm especially excited about. It should be a pretty fun summer all around!

---

## Example 23: Warm-casual email to a professor (chatty, not formal)

**Context:** professor is traveling and asked a question; reply is warm and conversational, shares own day, asks back about their plans
**Text:**
> Hi Professor Montoya,
>
> I'm not sure Scotland has much weather beyond drizzly and gray skies! But in my opinion that does seem to fit the academia atmosphere perfectly. I hope you're still enjoying the trip despite it. Since the Ocean Sciences meeting runs all week, do you have any plans to explore a bit while you're there?
>
> I'm actually living in Brookline, near BU, so just outside of Boston proper. It's a bit more residential and quieter, but still very convenient for commuting. I can easily get to Fenway via public transportation, which is where WHOOP is located. But with the blizzard this weekend, I was working from home today and will likely do the same tomorrow. Might go sledding once the wind calms down!

---

## Example 24: PR description (feature / new script)

**Context:** WHOOP-style PR template with Background / Definition of Done / In this PR sections; terse, bulleted, no pleasantries
**Text:**
> **Background**
>
> We want to evaluate the impact of Bloom nightly metrics on downstream menstrual cycle inference and trend outputs. Currently, MCI requests use production recovery metrics; this PR introduces `replace_recovery_metrics.py` which replaces those metrics with Bloom-derived nightly metrics or replaces all the metrics with null depending on what `metrics_type` is defined as. This enables us to do comparison of Bloom vs production vs no metric signals.
>
> **Definition of Done**
>
> There is a working step that replaces recovery metrics in MCI request JSONs with Bloom metrics, and the menstrual trend pipeline runs successfully using those updated inputs. The same applied for the step that replaces recovery metrics in MCI request JSONs with null metrics.
>
> **In this PR**
>
> Added `replace_recovery_metrics.py`, which:
> - Handles both Bloom and null paths based on a provided `metrics-type`
> - Reads `nightly_metrics.parquet` from WhoopDS inputs
> - Replaces `recovery_history` metrics in MCI request JSONs with Bloom values or nulls
>
> Added 3 days to the request timestamp in `prospective_historical_development_set_query.sql` to correct prospective prediction dates.
>
> Updated `launch.json` configs to support local runs of:
> - `replace_recovery_metrics.py`
> - `generate_menstrual_trends.py`

---

## Example 25: PR description (refactor / removal)

**Context:** PR removing unused code paths; same WHOOP template; bullets describe file-level changes
**Text:**
> **Background**
>
> The ovulation detection model trains purely on skin temperature. RR-interval-derived metrics (HRV, respiratory rate, HR-from-RR) were being computed and stored throughout the nightly metrics pipeline but never used as model features. Removing them simplifies the pipeline and reduces compute during metric rollup.
>
> **Definition of Done**
> - `MetricRollup` no longer stores or computes `hrv`, `respiratory_rate`, or `hr_from_rrs`
> - `NightlyMetrics` no longer stores or aggregates any of the 10 RR-derived fields
> - `DataQualityFilters` no longer exposes `apply_rr_data_quality_check_hrv` / `apply_rr_data_quality_check_resp_rate`
> - `MetricRollupProcessor` no longer instantiates `HRVCalculator` or `RespiratoryRateCalculator`
>
> **In this PR**
> - Updated `metric_rollup.py`: removed `hrv`, `respiratory_rate`, `hr_from_rrs` fields, dropped `HRVCalculator`/`RespiratoryRateCalculator`/`HRCalculator` imports, simplified `from_metric_window` signature
> - Updated `roll_up_metrics.py`: removed calculator instantiation from `MetricRollupProcessor.__init__`, updated `get_rollup` call
> - Updated `nightly_metrics.py`: removed 10 RR-derived model fields, removed `_calculate_hr_from_rrs_metrics`, `_calculate_hrv_metrics`, `_calculate_respiratory_rate_metrics` methods
> - Updated `data_quality_filters.py`: removed `apply_rr_data_quality_check_hrv` and `apply_rr_data_quality_check_resp_rate` from model and loader

---

## Example 26: Cold outreach email to a professor (course + research interest)

**Context:** emailing a professor whose class she just registered for, asking about undergrad research credits; ties personal experience to their lab's work
**Text:**
> Hi Professor McGrath,
>
> My name is Diya Sharma, and I am a rising senior majoring in Computer Science with a minor in Biology. I just registered for your Biological Programming course and also came across your research, which I found really interesting!
>
> I am especially drawn to the computational side of understanding animal behavior, and I think the work your lab is doing with cichlid fishes is very cool! Last year, I took a Behavioral Biology course in New Zealand, where I conducted a project studying the correlation between seagull vocalizations and their behavior. We used a prebuilt software to capture and analyze their calls since it was a 6-week class, but I really enjoyed the experience of combining biology with computational analysis.
>
> I would love the opportunity to get involved in your lab this fall, if there are any openings. Ideally, I am hoping to complete 2 Biology (BIOS 2699) Undergraduate Research credit hours toward my minor.
>
> I have attached my resume for your reference and would be happy to provide any additional information.
>
> Thank you for your time and consideration!
>
> Best regards,
> Diya Sharma
> Georgia Institute of Technology
> Computer Science
> 443-779-0236

---

## Example 27: Cold outreach email to a researcher (research role inquiry)

**Context:** more formal cold email to a PI in a specific research area; references their work specifically, proposes hours commitment
**Text:**
> Dear Dr. Dyer,
>
> My name is Diya, and I'm a rising third-year student studying computer science with threads in intelligence and people as well as a minor in neuroscience. I am very interested in computational neuroscience and am fascinated by neuroAI in particular. Recently, I was involved in data science and neuroscience research at the University of Maryland Baltimore School of Medicine at the Blanpied Lab.
>
> I am wondering if you have any availability in your lab for an undergraduate researcher during the fall. I noticed your work is currently focused on investigating class bias in classification models through spectral imbalance in features as well as latent space augmentation for improving deep learning model generalization. I would be eager to get involved in research similar to this, and I would love the opportunity to commit 10-15 hours a week toward a research project in your lab.
>
> I've attached my resume for your review. Please let me know if you have any questions! Thank you so much for your time.
>
> Sincerely,
> Diya Sharma

---

## Example 29: Short third-person bio (program / org page)

**Context:** brief third-person bio for a program directory or org member page; leads with school + major, then current research/activity, ends with a personal note
**Text:**
> Diya Sharma is a Computer Science major with a minor in Neuroscience at Georgia Tech. She is involved in the Smart Biosensors VIP program, where she researches applications of EEG, ECG, and other biosignals, exploring how AI and machine learning can be used to interpret and apply them in innovative ways. In her free time, Diya enjoys attending any and all Tech sporting events. Go Jackets!

---

## Example 30: LinkedIn-style first-person bio

**Context:** short first-person professional bio for LinkedIn / personal site landing; current role + interests + extracurriculars + link
**Text:**
> I'm a third-year Computer Science student at Georgia Tech and an Applied Machine Learning Science Co-op at WHOOP, where I get to combine my love for sports, technology, and data.
>
> Outside of the classroom, I'm a tour guide, a writer and photographer for The Technique, and I've traveled through two study abroad programs that shaped how I see the world. You can check out my portfolio and blog at diyasharma.vercel.app.

---

## Example 31: Portfolio project entry (resume-style bullets with framing)

**Context:** personal-website project entries; each has a one-line tagline, then 3–4 action-led bullets, then a tech-stack list. More polished than a raw resume. Has narrative framing on top.
**Text:**
> **TrainSmartAI** *(2025 to Present · Solo · design, ML, full stack)*
> A local-first health intelligence dashboard for Apple Health data.
> - Built a streaming XML parser to ingest multi-gigabyte Apple Health exports into PostgreSQL.
> - Designed a weighted daily readiness score across sleep, heart rate, training load, and bedtime consistency.
> - Implemented K-means clustering to auto-label day archetypes (hard training, deep recovery, balanced).
> - Engineered a LangChain RAG chat assistant with Chroma + Ollama embeddings running entirely on-device. No API keys, no cloud calls.
>
> *Stack:* FastAPI · PostgreSQL · pandas · scikit-learn · LangChain · Ollama · Streamlit
>
> ---
>
> **EEG-Based Stress & Workload Detection** *(Jan 2024 to Present · Undergraduate Research Assistant · Bio-Interfaced Translational Nanoengineering (BITN) Lab)*
> A wearable biosensor and deep-learning pipeline for real-time mental workload and stress detection.
> - Developed a wearable device prototype that monitors stress through EEG, ECG, and physiological signals.
> - Built data preprocessing pipelines: filtering, artifact removal, normalization, and feature extraction.
> - Trained and optimized deep learning models (CNN, BLSTM-LSTM) for biomedical signal classification.
> - Fabricated biocompatible hardware tailored for stress detection with EEG as the primary modality.
>
> *Stack:* EEG · Signal Processing · BLSTM-LSTM · CNN · Python · PyTorch · ICA · Wearable Hardware
>
> ---
>
> **Machine Learning-Driven Analysis of Synaptic Structures** *(Oct 2022 – Apr 2023 · Summer 2024 · Data Science Intern · UMD School of Medicine · Blanpied Lab)*
> A machine learning study of synaptic protein clusters across inhibitory neuron subtypes.
> - Developed a classification system (SVM, Random Forest, Gradient Boosting) to automatically differentiate synapses.
> - Applied feature engineering and dimensionality reduction techniques using scikit-learn.
> - Automated data collection and image processing pipelines in Java, MATLAB, and Python over confocal microscopy data.
> - Authored an upcoming first-author manuscript on synaptic protein cluster diversity across inhibitory neuron subtypes.
>
> *Stack:* Python · Java · MATLAB · scikit-learn · SVM · Random Forest · Gradient Boosting · Image Processing
>
> ---
>
> **Electronic Sensor for Mass Casualty Triage** *(June 2022 – Mar 2023 · Mechanical Engineering Intern · JHU APL)*
> A low-cost electronic triage tag designed to replace paper tags in mass casualty events.
> - Conceived the fully electronic triage tagging system concept, securing a $20,000 grant.
> - Led the intern team designing a novel medical sensor component (~$70 prototype).
> - Captured vital signs (blood oxygen, heart rate, temperature, and mobility) with an onboard LED status indicator.
> - Redesigned the prototype around a custom PCB for a compact, adhesive form factor.
> - Presented the research and prototype at the 2023 IEEE Integrated STEM Education Conference.
>
> *Stack:* CAD · PCB Design · Mechanical Product Design · Microcontrollers · Sensors · 3D Printing
>
> ---
>
> **CS 2340 · Objects and Design** *(Aug – Dec 2024 · Scrum Master · Team 5 · Georgia Tech CS 2340)*
> Two team projects from Georgia Tech CS 2340: a Spotify Wrapped clone and an Atlanta restaurant finder.
> - Served as Scrum Master across two team projects, coordinating a 5-member team through sprints and standups.
> - Built Spotify Wrapper, a year-round Spotify Wrapped clone, with Java-based Spotify Web API integration.
> - Built Atlanta Food Finder, a Django + Next.js restaurant discovery app on top of the Google Maps Places API.
> - Drove the OO design across both projects with use-case and sequence diagrams.
> - Delivered both projects ahead of deadline.
>
> *Stack:* Django · Next.js · Python · Java · TypeScript · Spotify Web API · Google Maps API · OAuth

---

## Example 32: Personal blog post (travel reflection)

**Context:** long-form personal blog reflecting on a goal she set and accomplished; narrative arc (set goal → chronological recap → lesson learned → closing thought); concrete details and place names; ends with a takeaway line
**Text:**
> When I first set my goal to visit 20 countries before turning 20, it felt like a dream that was probably too big to reach. But now I can say I did it and that the experience has been nothing short of amazing. Over the past year, I traveled to 14 countries in just 8 months, and every single trip taught me something new about the world and also about myself.
>
> My journey started with the Pacific Program from January to March. I spent six weeks in New Zealand and six weeks in Australia. These countries were breathtaking. New Zealand's landscapes looked like they were straight out of a movie (literally Lord of the Rings). From towering mountains to endless green hills, each view was more stunning than the last. Then Australia was vibrant and full of life from the beaches to the cities. We went to Townsville, Cairns, Magnetic Island, Port Douglas, and then spent three weeks in Sydney. During those weeks, I snorkeled in the Great Barrier Reef and sky dived in Cairns. Nothing could compare to that thrill.
>
> Before heading back to the states I stopped in Singapore and Japan. Singapore amazed me with its clean modern cityscape. I watched wild otters hunt near the Merlion during sunrise. In Japan, I saw cherry blossoms during their peak season and navigated Tokyo, the busiest city in the world.
>
> Then I joined the Barcelona Program from May to August. This was where my goal really picked up speed. I visited a new country each weekend. I went to Spain, Andorra, Switzerland (twice because I loved it so much), Greece, Germany, Morocco, the UK, Portugal, Scotland, and Ireland. Traveling so quickly from place to place was challenging, but it taught me the value of planning, flexibility, and making the most of every moment. Each country had its own charm, history, and flavor. Japan amazed me with its blend of tradition and modernity, Greece with its stunning islands, and Morocco with its colorful markets and deserts.
>
> Looking back, I'm incredibly grateful. Traveling young gave me more than just stamps in my passport. It gave me confidence, curiosity, and a sense of connection to the world. It showed me that goals are achievable if you're determined and that the experiences you gain from travel are far beyond what you can imagine.
>
> I set out to visit 20 countries before I turned 20, and I did it. But more than that, I've grown, learned, and collected memories I will carry forever. If there's one thing I've learned from traveling young, it's that the world is big, beautiful, and full of opportunities. And sometimes, all it takes is the courage to start exploring.

---

## Example 33: Personal blog post (event / experience reflection)

**Context:** shorter personal blog about a single event; scene-set opener, what she noticed in the moment, what she learned, ends with a forward-looking line
**Text:**
> Being on the sidelines for the Tech vs. UGA volleyball game at McCamish was one of the coolest experiences I've had. I wasn't there as a photographer but as a writer for the Technique. Still, I brought my camera and ended up joining the other Tech photographers on the sideline. The game had the biggest crowd in Tech volleyball history, and being right next to the players during such a huge rivalry made it even more special.
>
> Standing just a few feet away, I could hear the players calling to each other and feel the energy of every serve and spike. The game felt so much faster up close than it does from the stands. I tried taking some pictures, but I quickly realized how hard it is to capture action shots. By the time I focused, the ball was already on the other side of the court. I know I have a lot to learn about following the pace of the game and timing my photos.
>
> During the timeouts, I talked with the other photographers on the sideline. Some were from the Technique and gave me advice on taking better shots, while others were student interns for the athletic department. I asked them about their experience, and it was fun to hear what they enjoyed about working with Tech sports.
>
> Even though my pictures weren't perfect, I walked away with something better. I got the memory of standing on the court during one of the biggest volleyball nights in Tech history. It's not every day you get to experience a rivalry game from that close, and it made me even more excited to keep learning and improving.

---

## Example 28: Slack short PR / results follow-up

**Context:** concise update sharing a follow-up PR plus a one-paragraph result summary; offers next-step option
**Text:**
> Shorter follow up PR 331 (187 lines) for the 90th percentile and max distributions! The confluence doc has been updated with the results. The median time that the 90th percentile occurs is 1.2 hours after sleep start and for max it is 2.7 hours after. The distribution is pretty right skewed. I could probably increase the sample size. It didn't take too long to run.
