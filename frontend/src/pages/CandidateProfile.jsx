import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function CandidateProfile() {
  const { id } = useParams();

  const [data, setData] = useState(null);
  const [githubStats, setGithubStats] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/candidate/${id}`)
      .then((res) => res.json())
      .then((d) => {
        setData(d);

        // auto-load GitHub stats
        if (d.github_username) {
          loadGitHubStats(d.github_username);
        }
      });
  }, [id]);

  const loadGitHubStats = (username) => {
    fetch(`http://127.0.0.1:5000/github/${username}`)
      .then((res) => res.json())
      .then((stats) => setGithubStats(stats));
  };

  if (!data) return <h2 style={{ padding: "20px" }}>Loading profile...</h2>;

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Candidate Profile</h1>

      {/* ===== BASIC DETAILS ===== */}
      <p><b>Email:</b> {data.email}</p>
      <p><b>Phone:</b> {data.phone}</p>

      {/* ===== GITHUB STATS ===== */}
      <h2 style={{ marginTop: "30px" }}>GitHub Summary</h2>

      {!data.github_username && (
        <p>No GitHub username found in resume</p>
      )}

      {data.github_username && (
        <div
          style={{
            padding: "15px",
            background: "#f5f5f5",
            borderRadius: "10px",
            width: "420px",
            marginBottom: "20px"
          }}
        >
          <p><b>Username:</b> {data.github_username}</p>

          {!githubStats && <p>Loading GitHub stats...</p>}

          {githubStats && !githubStats.error && (
            <>
              <p><b>Repositories:</b> {githubStats.repo_count}</p>
              <p><b>Stars:</b> {githubStats.stars}</p>
              <p><b>Forks:</b> {githubStats.forks}</p>
              <p><b>Last Active:</b> {new Date(githubStats.last_active).toDateString()}</p>

              <h4>Languages</h4>
              <ul>
                {Object.keys(githubStats.languages).map((lang) => (
                  <li key={lang}>
                    {lang} ({githubStats.languages[lang]} repos)
                  </li>
                ))}
              </ul>

              <h4>Top Repositories</h4>
              <ul>
                {githubStats.top_repos?.map((repo) => (
                  <li key={repo.name}>
                    <a href={repo.url} target="_blank">
                      {repo.name}
                    </a>{" "}
                    ⭐ {repo.stars}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}

      {/* ===== SKILLS ===== */}
      <h3>Skills</h3>
      <ul>
        {data.skills.map((s) => (
          <li key={s}>{s}</li>
        ))}
      </ul>

      {/* ===== EXPERIENCE ===== */}
      <h3>Experience</h3>
      <pre>{data.experience}</pre>

      {/* ===== PROJECTS ===== */}
      <h3>Projects</h3>
      <pre>{data.projects}</pre>

      {/* ===== EDUCATION ===== */}
      <h3>Education</h3>
      <pre>{data.education}</pre>
    </div>
  );
}

export default CandidateProfile;
