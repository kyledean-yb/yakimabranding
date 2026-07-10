export type Review = {
  quote: string;
  name: string;
  initials: string;
  avatarBackground: string;
};

/** Google reviews from the home page (partials/reviews-scroll.html). */
export const GOOGLE_REVIEWS: Review[] = [
  {
    quote:
      "Yakima Branding's team is professional, creative, accommodating and very patient! We made several changes, pivoted on our initial concept, and they stay…",
    name: "Heather Hellums",
    initials: "HH",
    avatarBackground: "var(--grad-brand)",
  },
  {
    quote:
      "Yakima Branding is an excellent choice for all of your SEO, marketing, branding, logos, websites and more. Jacob is extremely knowledgeable and easy to …",
    name: "Josh DeBoer",
    initials: "JD",
    avatarBackground: "var(--grad-sunset)",
  },
  {
    quote:
      "Yakima Branding designed my website, hosts it and maintains the SEO. They are good at targeting the right clients for my business. High-quality services…",
    name: "Law Office",
    initials: "LO",
    avatarBackground: "linear-gradient(135deg,var(--yb-cyan),var(--yb-blue))",
  },
  {
    quote:
      "Great company to work with. I've completed two big projects and the business has been leaping up the Google results page with organic searches. I highly…",
    name: "Apex Dentures",
    initials: "AD",
    avatarBackground: "linear-gradient(135deg,var(--yb-pink),var(--yb-violet))",
  },
  {
    quote:
      "Worked with Jacob and his team and had a great experience building a new website! They were professional and easy to work with through the whole process.",
    name: "The Healthy Worker",
    initials: "TH",
    avatarBackground: "var(--grad-brand)",
  },
  {
    quote: "Great group to work with. Very knowledgeable and friendly.",
    name: "PMI Supplies",
    initials: "PS",
    avatarBackground: "var(--grad-sunset)",
  },
  {
    quote:
      "Had a great experience working with Jacob. He and his team guided us through developing a logo and initial branding. Looking forward to working with Yak…",
    name: "Groundwork Systems",
    initials: "GS",
    avatarBackground: "linear-gradient(135deg,var(--yb-pink),var(--yb-violet))",
  },
  {
    quote:
      "Yakima Branding was instrumental in the successful launch of my business and brand. Their creative ideas and mastery of technology and social media has …",
    name: "JLS Custom Construction",
    initials: "JC",
    avatarBackground: "var(--grad-sunset)",
  },
  {
    quote:
      "Jacob and Kyle came through on time when I needed a website rebuild with a tight deadline. They delivered a great product and were available on short no…",
    name: "Doug Turner",
    initials: "DT",
    avatarBackground: "var(--grad-sunset)",
  },
  {
    quote:
      "This company has been awesome. Jacob answered all my questions and did an awesome job with the website. He even dealt with Google when they suspended my…",
    name: "Luis Fernandez",
    initials: "LF",
    avatarBackground: "linear-gradient(135deg,var(--yb-cyan),var(--yb-blue))",
  },
  {
    quote:
      "Jacob and his team were awesome to work with in designing my law firm's website. They listened to our needs, were hands on, and made me feel comfortable…",
    name: "Emily Schwab",
    initials: "ES",
    avatarBackground: "linear-gradient(135deg,var(--yb-mint),var(--yb-cyan))",
  },
  {
    quote:
      "Jacob is knowledgeable, professional and extremely accommodating. Has helped us build our new site and we were so satisfied we're discussing additional …",
    name: "Kitt Murry",
    initials: "KM",
    avatarBackground: "linear-gradient(135deg,var(--yb-mint),var(--yb-cyan))",
  },
];

export const GOOGLE_REVIEW_COUNT = 43;
export const GOOGLE_RATING = "5.0";
