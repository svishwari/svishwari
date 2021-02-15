import React from 'react'
import { useLocation } from 'react-router-dom'

const Page = () => {
    const location = useLocation();
    const currentPath = location.pathname.split("/").map(word => (word.charAt(0).toUpperCase() + word.slice(1))).join(" ").trim()
    return (
        <div>
            {currentPath}
        </div>
    )
}

export default Page
