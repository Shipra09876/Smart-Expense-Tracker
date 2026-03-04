import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { AccountAPI } from "../Api/axios";

function Profile() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const inputStyle =
    "w-full p-3 rounded-xl bg-white/10 text-white outline-none focus:ring-2 focus:ring-purple-500";

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await AccountAPI.get("profile/");
      setProfile(res.data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await AccountAPI.put("profile/", profile);
      alert("Profile updated successfully 🚀");
    } catch (err) {
      console.log(err);
      alert("Update failed");
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-2xl mx-auto">

        <h1 className="text-3xl font-bold mb-8">My Profile</h1>

        {loading ? (
          <p className="text-gray-400">Loading profile...</p>
        ) : (
          <div className="bg-white/5 backdrop-blur-lg p-8 rounded-2xl shadow-xl">

            <form onSubmit={handleUpdate} className="space-y-5">

              {/* Email (readonly) */}
              <div>
                <label className="text-gray-400 text-sm">Email</label>
                <input
                  className={inputStyle}
                  value={profile.email || ""}
                  disabled
                />
              </div>

              {/* Name */}
              <div>
                <label className="text-gray-400 text-sm">Full Name</label>
                <input
                  className={inputStyle}
                  value={profile.name || ""}
                  onChange={(e) =>
                    setProfile({ ...profile, name: e.target.value })
                  }
                />
              </div>

              {/* Occupation */}
              <div>
                <label className="text-gray-400 text-sm">Occupation</label>
                <input
                  className={inputStyle}
                  value={profile.occupation || ""}
                  onChange={(e) =>
                    setProfile({ ...profile, occupation: e.target.value })
                  }
                />
              </div>

              {/* Monthly Income */}
              <div>
                <label className="text-gray-400 text-sm">Monthly Income</label>
                <input
                  type="number"
                  className={inputStyle}
                  value={profile.monthly_income || ""}
                  onChange={(e) =>
                    setProfile({
                      ...profile,
                      monthly_income: Number(e.target.value),
                    })
                  }
                />
              </div>

              {/* Currency */}
              <div>
                <label className="text-gray-400 text-sm">Currency</label>
                <input
                  className={inputStyle}
                  value={profile.currency || ""}
                  onChange={(e) =>
                    setProfile({ ...profile, currency: e.target.value })
                  }
                />
              </div>

              <button
                type="submit"
                className="w-full bg-purple-600 hover:bg-purple-700 
                           transition duration-300 p-3 rounded-xl 
                           text-white font-semibold"
              >
                Save Changes
              </button>

            </form>

          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Profile;