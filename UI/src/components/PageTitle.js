import React from "react";
import { Link } from "react-router-dom";
import "./PageTitle.scss";

const PageTitle = (props) => {
  return (
    <div className="pageTitle">
      {props.children}
      <div className="titleSection">
        <h2>{props.title}</h2>
        <span>
          {props.summaryText}
          <Link to={props.readMore}>{props.readMoreLabel}</Link>
        </span>
      </div>
    </div>
  );
};

export default PageTitle;
