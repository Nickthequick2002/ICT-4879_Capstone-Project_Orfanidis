/** This script handles the serach bar of the website.
 * Takes the user's search input and matches it with a large keyword map
 * and redirects the user to the most relevant section or page
 */

const searchInput = document.getElementById("navSearch");
const searchBtn = document.getElementById("searchBtn");

function redirectToPage() {
  const query = searchInput.value.trim().toLowerCase();
  if (!query) return;

  // This is the search map that defines all the keywords the user may type 
  // and the destination for that group 
  const searchMap = [
    {
      keywords: [
        "bmi", "body mass index", "weight", "height", "fat", "obesity", "measure", "calculator",
        "body analysis", "fitness score", "ideal weight", "bmi calculator", "check bmi",
        "calculate weight", "body measurement", "weight index", "fat level", "body metrics"
      ],
      url: "/#bmi"
    },
    {
      keywords: [
        "calories", "mycals", "nutrition", "diet", "food", "meal", "eating", "intake", "tracker",
        "macros", "protein", "carbs", "fats", "daily calories", "nutrition plan", "meal plan",
        "diet plan", "food log", "meal tracking", "nutrition tracker", "calorie counter",
        "healthy eating", "nutrition facts", "macro calculator", "nutrition advice", "weight loss"
      ],
      url: "/mycals/"
    },
    {
      keywords: [
        "programs", "training", "workout", "exercise", "routine", "fitness", "plan", "gym",
        "home training", "strength", "cardio", "abs", "legs", "arms", "chest", "schedule",
        "training plan", "workout program", "fitness class", "daily exercise", "gym training",
        "personal training", "stretching", "yoga", "core", "upper body", "lower body", "hiit",
        "training session", "fittrack workouts"
      ],
      url: "/#programs"
    },
    {
      keywords: [
        "contact", "email", "support", "help", "message", "form", "get in touch", "reach us",
        "feedback", "customer service", "assistance", "contact form", "technical support",
        "customer help", "report problem", "send message", "ask question", "inquiry",
        "contact us", "connect", "get support"
      ],
      url: "/contact/"
    },
    {
      keywords: [
        "about", "mission", "team", "story", "who we are", "our goal", "values", "vision",
        "company info", "fittrack story", "about fittrack", "our team", "company background",
        "history", "team members", "brand story", "about us", "meet the team", "company mission",
        "objectives", "goals", "our purpose"
      ],
      url: "/aboutus/"
    },
    {
      keywords: [
        "shop", "fitshop", "store", "products", "buy", "equipment", "merch", "supplements",
        "fittrack store", "shop now", "gear", "order", "purchase", "items", "fitness gear",
        "merchandise", "online shop", "buy products", "shop items", "accessories", "store page",
        "supplement store", "buy equipment", "shop fittrack", "buy now"
      ],
      url: "/fitshop/"
    },
    {
      keywords: [
        "home", "main", "index", "homepage", "start", "dashboard", "fittrack home",
        "go home", "return home", "main page", "welcome", "landing", "front page"
      ],
      url: "/"
    },
  ];

  // Break query into individual words to support the multi-word matching
  const queryWords = query.split(/\s+/);
  let destination = null;


  /** The matching logic is really simple.
   * It joins all the keywords into a one big string checks whether
   * every word the user typed appears somewhere inside that string
   */
  for (const entry of searchMap) {
    const joinedKeywords = entry.keywords.join(" ").toLowerCase();

    const allMatch = queryWords.every(word =>
      joinedKeywords.includes(word)
    );

    if (allMatch) {
      destination = entry.url;
      break;
    }
  }

  // If a match is found, redirects the user
  if (destination) {
    window.location.href = destination;
  } else {
    // Simple fallback if nothing matched
    alert(`No results found for "${searchInput.value}".`);
  }

  searchInput.value = "";
}

// Click handler on the search button
searchBtn.addEventListener("click", (e) => {
  e.preventDefault();
  redirectToPage();
});

// Allow pressing Enter to search
searchInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    redirectToPage();
  }
});
