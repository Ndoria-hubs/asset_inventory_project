import React from "react";

const Admin_dash = () => {
    function handleAssetClick(params) {
        // direct to assets when clicked - all
        pass
    }
    function handleViewReportsClick(params) {
        // direct to assets when clicked
        // admin - protected route
        pass
    }
    function handleCategoryClick(params) {
        // direct to category when clicked - all
        pass
    }
    function handleViewReportsClick(params) {
        // direct to assets when clicked
        // admin - protected route
        pass
    }

    function handleViewRequestsClick(params) {
        // direct to assets when clicked
        // protected route
        pass
    }
    function handleUserManClick(params) {
        // direct to users when clicked - user
        // should have a drop down for users

        {/* // pass */}
    }

    return (
        <div>
        <div>admin_dash</div>
        <div>
            <ul>
                <li> Assets </li>
                <li> Categories </li>
                <li> Requests </li>
                <li> Reports </li>
                <li><select> User Management </select>
                    <option> User 1 </option>
                    <option> User 2 </option>
                    <option> User 3 </option>
                    <option> User 4 </option>
                    <option> User 5 </option>
                </li>
            </ul>
            </div>
        </div>

    )
}

export default Admin_dash;
