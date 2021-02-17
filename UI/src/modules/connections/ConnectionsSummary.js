import React from "react";
import PageTitle from "../../components/PageTitle";
import { ReactComponent as TitleImage } from "../../assets/ConnectionsTitle.svg";

const ConnectionsSummary = () => {
  return (
    <>
      <PageTitle
        title="Connections"
        summaryText={"Lorem ipsum."}
        readMore="/"
        readMoreLabel="Learn More"
      >
        <TitleImage />
      </PageTitle>
    </>
  );
};
export default ConnectionsSummary;
