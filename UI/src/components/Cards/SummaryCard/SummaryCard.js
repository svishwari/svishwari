import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import CountUp from "react-countup";

const useStyles = makeStyles(() => ({
  section: {
    display: "flex",
    flexDirection: "column",
    background: "#FFFFFF",
    border: "1px solid #D0D0CE",
    boxSizing: "border-box",
    borderRadius: "5px",
    boxShadow: "none",
    padding: "10px",
    margin: "10px"
  },
  title: {
    fontFamily: "Open Sans SemiBold",
    fontStyle: "normal",
    fontWeight: 600,
    fontSize: "12px",
    lineHeight: "16px",
    letterSpacing: "0.2px",
    color: "#767676",
    paddingBottom: "10px",
  },
  valueStyle: {
    fontFamily: "Open Sans SemiBold",
    fontStyle: "normal",
    fontWeight: "bold",
    fontSize: "16px",
    lineHeight: "24px",
    letterSpacing: "0.1px",
    color: "#333333",
  },
}));

const SummaryCard = ({hasAnimation=true,width,title,value,...props}) => {
  const classes = useStyles();
  return (
    <Paper style={{width: width || "150px" }} elevation={3} className={classes.section}>
      {title ? <span className={classes.title}>{title}</span> : ""}
      {
        hasAnimation ?
        <CountUp
          start={0}
          end={value}
          delay={1}
          {...props}
          className={classes.valueStyle}
        />
        : <span className={classes.valueStyle}>{value}</span>
      }
    </Paper>
  );
};

export default SummaryCard;
