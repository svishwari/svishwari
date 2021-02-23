import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Link } from "react-router-dom";
import PageTitle from "../../components/PageTitle";
import { ReactComponent as TitleImage } from "../../assets/ConnectionsTitle.svg";
import SummaryCard from "../../components/Cards/SummaryCard/SummaryCard";
import CTList from "../../components/List/List";

const useStyles = makeStyles(() => ({
  contentWrapper: {
    padding: "38px 60px 0px 70px",
  },
  section: {
    display: "flex",
    flexDirection: "column",
  },
  sectionTitle: {
    display: "flex",
    justifyContent: "space-between",
  },
  sectionTitleHeading: {
    fontFamily: "Open Sans SemiBold",
    fontStyle: "normal",
    fontWeight: 600,
    fontSize: "16px",
    lineHeight: "24px",

    letterSpacing: "0.1px",
    color: "#333333",
  },
  sectionTitleHeadingLink: {
    fontFamily: "Open Sans SemiBold",
    fontStyle: "normal",
    fontWeight: 600,
    fontSize: "14px",
    lineHeight: "22px",

    letterSpacing: "0.3px",
    color: "#0076A8",
  },
}));

const summaryContent=[
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
  {value: "20",suffix: "%",title: "Bogus"},
];

const ConnectionsSummary = () => {
  const classes = useStyles();
  const dataSourcesColumns = [
    {
      field: "name",
      headerName: "Source",
      flex: 0.6,
      renderCell: (params) => (
        <Link to={() => false}>
          {params.getValue("name")}{" "}
          <span
            className="iconify"
            data-icon="mdi:open-in-new"
            data-inline="false"
          />
        </Link>
      ),
    },
    {
      field: "filesCount",
      headerName: "No. of Files",
      flex: 0.4,
    },
  ];
  const dataSourcesData = [
    {
      id: 1,
      name: "Client",
      filesCount: 3,
    },
    {
      id: 2,
      name: "Amazon S3",
      filesCount: 50,
    },
  ];
  const destinationColumns = [
    {
      field: "name",
      headerName: "Destination",
      flex: 0.7,
      renderCell: (params) => (
        <Link to={() => false}>
          <span
            className="iconify"
            data-icon={`mdi:${params.getValue("icon")}`}
            data-inline="false"
          />
          {params.getValue("name")}{" "}
          <span
            className="iconify"
            data-icon="mdi:open-in-new"
            data-inline="false"
          />
        </Link>
      ),
    },
    {
      field: "account",
      headerName: "Account",
      flex: 0.3,
    },
  ];
  const destinationData = [
    {
      id: 1,
      name: "Facebook Insights",
      icon: "facebook",
      account: "Pendleton",
    },
    {
      id: 2,
      name: "Google Analytics",
      icon: "google-analytics",
      account: "Pendleton",
    },
    {
      id: 3,
      name: "Salesforce Marketing Cloud",
      icon: "salesforce",
      account: "Pendleton",
    },
  ];
  return (
    <>
      <PageTitle
        title="Connections"
        summaryText="Lorem ipsum."
        readMore="/"
        readMoreLabel="Learn More"
      >
        <TitleImage />
      </PageTitle>
      <div className={classes.contentWrapper}>
        <div className="row">
          <div className="col-md-6 col-xs-12">
            <div className={classes.section}>
              <div className={classes.sectionTitle}>
                <h3 className={classes.sectionTitleHeading}>
                  <Link to="/connections/data-sources">Data Sources &gt;</Link>
                </h3>
                <Link href={() => false} className={classes.sectionTitleHeadingLink}>
                  + DataSource
                </Link>
              </div>
              <div className="row">
                {summaryContent.map(content =>
                  <SummaryCard width="190px" value={content.value} suffix={content.suffix} title={content.title}/>
                )}
              </div>
              <div className="mt-5">
                <CTList
                  columns={dataSourcesColumns}
                  rows={dataSourcesData}
                  className="mt-5"
                />
              </div>
            </div>
          </div>
          <div className="col-md-6 col-xs-12">
            <div className={classes.section}>
              <div className={classes.sectionTitle}>
                <h3 className={classes.sectionTitleHeading}>
                  <Link to="/connections/data-sources">Destinations &gt;</Link>
                </h3>
                <Link href={() => false} className={classes.sectionTitleHeadingLink}>
                  + Destination
                </Link>
              </div>
            </div>
            <CTList columns={destinationColumns} rows={destinationData} />
          </div>
        </div>
      </div>
    </>
  );
};
export default ConnectionsSummary;
