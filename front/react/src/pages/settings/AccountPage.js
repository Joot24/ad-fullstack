import React, { useEffect, useState, useContext } from 'react';
import UpdatePassword from "../../components/user/UserUpdatePassword";
import UpdateEmail from "../../components/user/UserUpdateEmail";
import useUser from "../../hooks/useUser";
import { AuthContext } from "../../context/AuthContext";

const AccountPage = () => {
    const { isAuthenticated } = useContext(AuthContext);
    const { user, getUserDetails } = useUser();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                await getUserDetails();
                setLoading(false);
            } catch (error) {
                console.error("Error fetching user details:", error);
            }
        };
        fetchData();
    }, [getUserDetails]);

    if (!isAuthenticated) {
        return <div>Please log in to view this page.</div>;
    }

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Account Settings</h2>
            {user && <UpdateEmail user={user} />}
            {user && <UpdatePassword user={user} />}
        </div>
    );
};

export default AccountPage;
