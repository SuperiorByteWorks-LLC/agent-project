# Zero Trust for AI Agents - Source Material

> **Source:** IBM Video - "Securing AI Agents with Zero Trust"  
> **URL:** https://www.youtube.com/watch?v=d8d9EZHU7fw  
> **Transcription Date:** 2026-02-21  
> **Tool:** whisper-ctranslate2

---

## Full Transcription

[00:00.000 --> 00:05.920] We've entered the age of agentic AI systems that don't just think, but they also act.

[00:06.560 --> 00:12.720] Agents can talk to APIs, they can call tools, they can buy things, they can move data,

[00:12.720 --> 00:19.280] even create sub-agents. But every new capability adds a new attack surface, yet another way

[00:19.280 --> 00:24.720] the bad guys can get into our systems. So how do we protect this new ecosystem?

[00:24.720 --> 00:32.320] We bring zero trust, never trust, always verify. I know, I know, you've heard about zero trust before,

[00:32.320 --> 00:37.200] isn't that just a marketing slogan that all the vendors used and abused in order to get us to

[00:37.200 --> 00:42.240] buy whatever they had on the truck? Well, yes and no. Definitely the term got hijacked by

[00:42.240 --> 00:47.840] overzealous sellers trying to meet their quotas, but I'm a cybersecurity architect and I never

[00:47.840 --> 00:52.480] got confused by all that noise because I knew there were some solid, even game-changing

[00:52.480 --> 00:58.480] security principles worth holding on to. And now that we have AI agents popping up everywhere,

[00:58.480 --> 01:04.320] the time is right to dust off the hype and repurpose the good in zero trust in order to face

[01:04.320 --> 01:09.920] the current security challenge. Okay, let's take a quick review of what zero trust principles are,

[01:09.920 --> 01:14.720] what distinguishes zero trust from doing things in a non-zero trust way. Well,

[01:14.720 --> 01:19.680] one of the simple things that I mentioned previously is you verify and then you trust.

[01:19.680 --> 01:25.600] So, you only trust something that has in fact been verified or trust follows verification is

[01:25.600 --> 01:31.120] another way to think of it. Another thing is we get rid of the just-in-case principle where we

[01:31.120 --> 01:36.960] put things out in case we need them and replace it with just-in-time. So, we give the access

[01:36.960 --> 01:42.320] rights that are needed only when they're needed and not for longer than they're needed. That's

[01:42.320 --> 01:47.840] preserving of the principle of least privilege, which says you have only the access rights

[01:47.840 --> 01:53.200] that you need for only as long as you need them and not longer. Another thing is we move

[01:53.200 --> 01:59.760] from perimeter-based controls where we're trying to basically put the hard, crunchy outside and

[01:59.760 --> 02:05.360] leave the soft, chewy center. That's not very good. In fact, what we want to move to is a more

[02:05.360 --> 02:11.760] pervasive set of security controls. So, the security controls are throughout the system,

[02:11.760 --> 02:16.880] not just around the outside. And then what I think is the most important aspect and it

[02:16.880 --> 02:23.360] often gets overlooked in zero trust discussions is the idea of the assumption of breach. You assume

[02:23.360 --> 02:28.960] the bad guy is already in your system, already in your network, already in your database, in your

[02:28.960 --> 02:35.520] application, already has elevated privileges from stolen credentials. That's what we're going to

[02:35.520 --> 02:41.440] operate from. Now design your security. So, it's assuming that you've been breached already

[02:41.440 --> 02:46.080] and it's a very different model, a very different paradigm and way of thinking about security.

[02:46.080 --> 02:50.800] So, let's take a look and see what zero trust principles would look like if they were applied

[02:50.800 --> 02:55.840] to an agentic environment. First of all, let's look at a traditional environment. How do we

[02:55.840 --> 03:00.800] apply zero trust in this case? Well, we've got users that have to be secured. They're part of

[03:00.800 --> 03:06.160] the security equation. So, I need to do identity and access management. I need to make sure

[03:06.160 --> 03:10.320] that the user has an account, that they're logged in, that the person logged in is in fact the

[03:10.320 --> 03:16.320] user they claim to be. So, that's strong authentication. Access controls so that they can only access

[03:16.320 --> 03:21.920] the things that they're permitted to see. The device that the user is using matters as well.

[03:21.920 --> 03:27.600] It could be compromised. I need to make sure that it is in fact pure, that it hasn't been jail

[03:27.600 --> 03:32.880] broken, that an attacker hasn't taken control of the system because then it won't matter if I

[03:32.880 --> 03:38.640] have the authentic user trying to do the right thing if the device has already been compromised.

[03:38.640 --> 03:44.080] I need to look at the data layer of all of this. So, I need to make sure that the data that's sensitive

[03:44.080 --> 03:49.920] has been encrypted so it can't be easily seen. I need to make sure that it's not leaving my network

[03:49.920 --> 03:55.440] if it's not supposed to, things like that. And then another big part and a lot of people start

[03:55.440 --> 04:00.960] their zero trust discussions in this particular area and it's the area of the network. So, I'm

[04:00.960 --> 04:06.880] going to make sure that my network is well secured, that if information is traversing a part

[04:06.880 --> 04:12.480] and that information is sensitive, then I want to have it encrypted. I want to make sure that I do

[04:12.480 --> 04:17.920] things like micro segmentation, where I group individual parts of the network together and give

[04:17.920 --> 04:24.320] some level of isolation so that if this guy gets infected, his infection doesn't easily spread to

[04:24.320 --> 04:28.720] others. So, those are some of the things that we've done traditionally in zero trust

[04:28.720 --> 04:34.400] and spreading this pervasively throughout the system. I've got to do all of that

[04:34.480 --> 04:40.880] as I move into the agentic world, plus I have to do some more. So, as we start looking at agents,

[04:40.880 --> 04:48.480] who are the actors? The actors are in fact software. So, we've got an AI agent here that is

[04:49.760 --> 04:55.920] using a non-human identity. So, here we had users and we could associate them with the

[04:55.920 --> 05:00.640] identity they were using, but an agent may in fact use lots of these different

[05:00.640 --> 05:06.720] NHIs, lots of different non-human identities. So, here we have a proliferation of these things

[05:06.720 --> 05:13.840] growing. I need to make sure all of them have the same level of control and visibility that we had

[05:13.840 --> 05:18.720] for the human users. In fact, maybe even more because they're operating autonomously and we

[05:18.720 --> 05:24.560] need supervision of that. We need tools that we're going to be using to also be secure.

[05:24.560 --> 05:28.560] We need to make sure that the tools that we're leveraging are tools we can trust.

[05:29.280 --> 05:35.760] Again, we have data. In this case, data may be the thing that was the basis for the AI agent.

[05:35.760 --> 05:41.760] We use data to train the model. We need to also augment the model. We may use preference

[05:41.760 --> 05:47.200] information and other context information that we put into the model. I need to make sure all of

[05:47.200 --> 05:52.640] that stuff has been secured that it hasn't been tampered with. And then ultimately,

[05:52.640 --> 05:57.040] I need to be able to look at the intentions of the agent and make sure those intentions

[05:57.040 --> 06:01.920] match what the original user's intentions were for this particular system.

[06:01.920 --> 06:05.760] Let's take a look at an agentic system and see where the threats might be.

[06:05.760 --> 06:10.560] So, here's how the thing basically works. We have a sensing portion. That is the thing that

[06:10.560 --> 06:15.440] takes the input. It might be visual. It might be textual. It could be a lot of different things.

[06:15.440 --> 06:21.520] But that feeds into the AI which does the thinking. And then in that thinking, we will

[06:21.520 --> 06:26.320] augment that with policies, preferences, and other things like that. So, we'll have that

[06:26.320 --> 06:31.440] information affecting the thought process, the reasoning process that's happening. And then,

[06:31.440 --> 06:37.840] ultimately, it takes those actions. So, it could do an API call. It might write some data, move

[06:37.840 --> 06:44.560] some data around. It might use a tool. It might spawn other agents. And then all of this is going

[06:44.560 --> 06:50.000] to be driven by credentials. So, we have individual capabilities that each one of

[06:50.000 --> 06:54.720] these things ought to be able to have. So, if I'm an attacker, I look at this thing and

[06:54.720 --> 07:01.120] start to figure, how might I break this thing? Well, one thing I could do right here is a direct

[07:01.120 --> 07:07.040] prompt injection. I might send a prompt in that is going to break the context of this system

[07:07.040 --> 07:11.040] and have it start doing things that it's not supposed to do. So, that's one of the things

[07:11.040 --> 07:17.040] I could think about. Another is, I could attack right here and I could do something to manipulate

[07:17.040 --> 07:22.240] to mess up the policy, the preference information, to poison that information,

[07:22.240 --> 07:26.800] or even poison the model that was used to train this thing. So, that's another one to look at.

[07:27.600 --> 07:33.520] Another thing here is looking at all of these interfaces. What if I insert myself at any one

[07:33.520 --> 07:39.920] of these? That would be a place where I could do some damage if on this, and this might be, say,

[07:39.920 --> 07:46.240] an MCP call, something along those lines, and I would be able to insert and take control of

[07:46.240 --> 07:52.400] that. I might also attack individuals of these services, these APIs, the data source, the tools,

[07:53.040 --> 07:58.320] the agents. So, all of those are an extension of the attack surface. And then right here,

[07:58.320 --> 08:03.920] they're credentials. Maybe I want to go in and attack those. Maybe I can copy those credentials.

[08:03.920 --> 08:10.160] Maybe I can log into a system and create new accounts or increase my level of privilege.

[08:10.160 --> 08:15.840] So, there's a lot of different moving parts in this system. An attacker has a wealth of

[08:15.840 --> 08:21.200] different places that they could, in fact, dive into and do a lot of damage. So, now let's apply

[08:21.200 --> 08:27.120] those zero trust principles to this AI agentic environment. And we'll see what we can do to

[08:27.120 --> 08:32.160] eliminate some or all of these threats. So, first of all, we're going to start here with the

[08:32.160 --> 08:36.800] credentials. And I mentioned this before. We want unique credentials for every agent,

[08:36.800 --> 08:41.760] for every user, and every agent that those agents create as well. So, we need a place to

[08:41.760 --> 08:47.280] store all of these non-human identities and keep all of them access controlled,

[08:47.280 --> 08:52.720] keep them so that they don't have more privilege than they're supposed to have. We want it to be

[08:52.720 --> 08:58.160] just in time, not just in case. In other words, we give the privilege just when it's needed,

[08:58.160 --> 09:01.760] and then we take it away. We don't give it in advance and say, well, just in case you might

[09:01.760 --> 09:06.000] need this later. So, we're going to do that. We're going to make sure that these systems

[09:06.080 --> 09:13.120] also never include credentials buried into the system itself. And that's been a temptation

[09:13.120 --> 09:20.240] of programmers. They put a password, they put an API key, and they embed it directly into their code.

[09:20.240 --> 09:25.840] That is an absolute no-no. What we want instead is to store all of these in a vault,

[09:25.840 --> 09:31.760] where we have a dynamic system where I can go check credentials in and out. I can get new

[09:31.760 --> 09:39.200] credentials created over time. I can enforce just in time. I can enforce role-based access control.

[09:39.200 --> 09:44.480] I can do strong authentication. I can do all of those kinds of things that I'm needing to do

[09:44.480 --> 09:50.880] in these cases. So, we're going to cover all of those bases, no static credentials,

[09:50.880 --> 09:56.560] everything is dynamic instead. And then we're going to move over to the tools themselves. So,

[09:56.560 --> 10:02.880] I need to make sure that these things have registered versions. So, I'm going to have a tool

[10:02.880 --> 10:10.560] registry where I have verified these are secure APIs that we can afford to use. The others have not

[10:10.560 --> 10:17.680] been vetted. These are a set of secure databases and data sources that we can use. These are a set

[10:17.680 --> 10:22.880] of tools that we have vetted and we can trust. And all of these kinds of things, if we're going

[10:22.960 --> 10:28.160] to be using those, basically think about if you're making a cake or a soup, you want to make sure that

[10:28.160 --> 10:32.640] the ingredients that go into it are pure. So, we want to make sure that we're using the pure

[10:32.640 --> 10:37.920] stuff to begin with. Then, I need something that's going to give me some sort of inspection

[10:37.920 --> 10:43.120] over the whole thing. So, something that's going to be able to look over it all, look here and

[10:43.120 --> 10:49.520] see if there are improper inputs going into any of these tools that are coming out of the agent.

[10:49.520 --> 10:55.040] Also, be able to look and check for these prompt injections that may be coming into the system.

[10:55.040 --> 11:02.000] We could use an AI firewall or an AI gateway, whichever term you prefer, to do those sort of checks

[11:02.000 --> 11:06.720] and block. So, it will look and see, is that something that should be allowed to go in?

[11:06.720 --> 11:11.760] Do we have information leaking out of systems that shouldn't be? Are we making improper calls

[11:11.760 --> 11:16.480] this sort of thing? So, it's an enforcement layer here as well. And then, ultimately,

[11:16.480 --> 11:23.200] I need to be able to have traceability of all of this. So, I need a system where I'm logging immutable

[11:23.200 --> 11:28.160] logs. That means that they can't be changed. I don't want a bad guy to come in here and change the

[11:28.160 --> 11:33.200] information that's in my log. I want to be able to prevent that. So, when actions are occurring

[11:33.200 --> 11:38.880] in the system, it needs to be able to be traceable so we can go back later and understand why it

[11:38.880 --> 11:45.440] did what it did. I also want to scan the entire environment, be able to look across all of

[11:45.440 --> 11:49.200] these different things. And we've got different tools for different types of scanning. We've got

[11:49.200 --> 11:56.080] network scanning tools. We've got endpoint scanning tools. We've got tools now that can scan AI models

[11:56.080 --> 12:02.000] and look for vulnerabilities that may be latent and hiding inside of those. Ultimately, at the end

[12:02.000 --> 12:08.400] of all this, we need still a human in the loop. We need an ability to be able to have a kill

[12:08.400 --> 12:13.280] switch. If someone sees this thing is running out of control, what it's doing is not right

[12:13.280 --> 12:18.800] and we can go see what it's been doing. We want to put throttles in place in some cases

[12:18.800 --> 12:24.320] so that if maybe it's a bad buying application, it doesn't just suddenly decide, hey, I like this.

[12:24.320 --> 12:28.080] I'm going to buy a thousand of these in a minute. Maybe we don't want it to do that. So,

[12:28.080 --> 12:33.600] we throttle back its activity. We have canary deployments where we drop the canary in the

[12:33.600 --> 12:39.520] coal mine to see what happens. So, we're going to see if this system dropped into an environment

[12:39.520 --> 12:46.240] is going to operate properly or not. A lot of different things you can see here. The agent systems

[12:46.240 --> 12:53.120] are complex. The number of threats that we face are complex and numerous, so our security

[12:53.120 --> 13:01.680] defenses have to be up to the challenge. Agentic AI multiplies power and risk. Zero

[13:01.680 --> 13:06.960] trust gives us the framework to keep that power contained. Every agent must prove who it is,

[13:06.960 --> 13:12.720] justify what it wants and earn trust continuously. As we move forward with autonomous system,

[13:12.720 --> 13:18.320] zero trust principles deployed correctly serve as guardrails that keep innovation in alignment

[13:18.320 --> 13:31.200] with our intent instead of the bad guys.

---

## Key Concepts Extracted

### Zero Trust Principles (Core)

1. **Verify, Then Trust**
   - Only trust what has been verified
   - Trust follows verification

2. **Just-In-Time Access**
   - Replace "just-in-case" with "just-in-time"
   - Give access rights only when needed
   - Take away immediately after use

3. **Least Privilege**
   - Only the access rights you need
   - Only for as long as you need them
   - No longer, no more

4. **Pervasive Controls**
   - Move from perimeter-based (hard outside, soft inside)
   - To pervasive controls throughout the system
   - Security everywhere, not just at the edge

5. **Assumption of Breach** (Most Important)
   - Assume the bad guy is already in your system
   - Already in network, database, application
   - Already has elevated privileges
   - Design security from this premise

### Agentic vs Traditional Security

| Aspect          | Traditional           | Agentic                       |
| --------------- | --------------------- | ----------------------------- |
| **Actors**      | Human users           | Software agents               |
| **Identity**    | User accounts         | Non-human identities (NHIs)   |
| **Scale**       | One identity per user | Many NHIs per agent           |
| **Autonomy**    | Human-directed        | Autonomous operation          |
| **Supervision** | Human oversight       | Requires automated monitoring |

### Agentic System Architecture

**Input → Processing → Output → Actions**

1. **Sensing Layer** - Takes input (visual, textual, etc.)
2. **AI Processing** - Does the thinking/reasoning
   - Augmented with policies, preferences
3. **Actions** - Executes
   - API calls
   - Data movement
   - Tool usage
   - Spawning sub-agents
4. **Credentials** - Drives all capabilities

### Attack Vectors (Threats)

1. **Prompt Injection** - Direct attack on input
2. **Training Data Poisoning** - Compromise the model
3. **Interface Manipulation** - Insert into MCP/tool calls
4. **Service Compromise** - Attack APIs, data sources, tools
5. **Credential Theft** - Steal credentials, escalate privileges

### Zero Trust Defenses for Agents

1. **Credential Vault**
   - Unique credentials for every agent/user
   - Dynamic credential checkout
   - No static credentials in code
   - Just-in-time privilege
   - Role-based access control

2. **Tool Registry**
   - Register and verify tools
   - Vetted/secure APIs only
   - Verified data sources
   - "Pure ingredients" approach

3. **AI Firewall/Gateway**
   - Inspect all inputs to tools
   - Check for prompt injections
   - Block information leakage
   - Enforce proper calls

4. **Logging & Traceability**
   - Immutable logs (can't be changed)
   - Traceable actions
   - Understand why agent did what it did

5. **Scanning**
   - Network scanning
   - Endpoint scanning
   - AI model vulnerability scanning

6. **Human Controls**
   - Human in the loop
   - Kill switch
   - Throttles (prevent runaway actions)
   - Canary deployments

### Key Quotes

> "Every new capability adds a new attack surface"

> "Never trust, always verify"

> "Verify and then you trust - trust follows verification"

> "Assumption of breach is the most important aspect"

> "Assume the bad guy is already in your system"

> "Agentic AI multiplies power and risk"

> "Zero trust gives us the framework to keep that power contained"

> "Every agent must prove who it is, justify what it wants, and earn trust continuously"

> "Zero trust principles serve as guardrails that keep innovation in alignment with our intent instead of the bad guys"

---

**Source Video:** https://www.youtube.com/watch?v=d8d9EZHU7fw  
**Title:** Securing AI Agents with Zero Trust  
**Speaker:** IBM Cybersecurity Architect  
**Duration:** ~13 minutes  
**Transcribed:** 2026-02-21
