import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Data management > Email Deliverability", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.emailDeliverability)
  })

  it("should have an Overview, Delivered Count/Open Rate chart, Sending domain overview table and domain charts", () => {
    cy.location("pathname").should("eq", route.emailDeliverability)

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)

    // should be able to view overview of email deliverability"
    cy.get(selector.emailDeliverability.overview).should("exist")

    // should be able to check if valid response for delivered count/open rate has received"
    cy.get(selector.emailDeliverability.deliveredChart)
      .its("length")
      .should("gt", 0)

    // Verifying the table columns names of the Sending Domain Overview Table
    const tableHeadersSendingDomainOverview = [
      "Domains",
      "Sent",
      "Bounce rate",
      "Open rate",
      "Click rate",
    ]

    const tableHeadersSendingDomain = [
      "Domains",
      "Sent",
      "Bounce rate",
      "Open rate",
      "Click rate",
    ]

    cy.get(
      selector.emailDeliverability.sendingDomainOverview.domainOverviewTable,
    )
      .find(
        selector.emailDeliverability.sendingDomainOverview.overviewTableHeaders,
      )
      .children()
      .each(($elm, i, $lis) => {
        if ($lis.length == tableHeadersSendingDomainOverview.length) {
          expect($elm.text()).equal(tableHeadersSendingDomainOverview[i])
        } else {
          expect($elm.text()).equal(tableHeadersSendingDomain[i])
        }
      })

    cy.get(
      selector.emailDeliverability.sendingDomainOverview.domainOverviewTable,
    )
      .find(
        selector.emailDeliverability.sendingDomainOverview.overviewTableItems,
      )
      .children()
      .its("length")
      .should("be.gt", 0)

    // should be able to check if valid response for sent domain charts has received"
    cy.get(selector.emailDeliverability.sentDomain)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for delivered rate domain charts has received"
    cy.get(selector.emailDeliverability.deliveredRateDomain)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for open rate domain charts has received"
    cy.get(selector.emailDeliverability.openRateDomain)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for click rate domain charts has received"
    cy.get(selector.emailDeliverability.clickRateDomain)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for sent unsubscribe rate charts has received"
    cy.get(selector.emailDeliverability.unsubscribeRateDomain)
      .its("length")
      .should("gt", 0)

    // should be able to check if valid response for complains rate domain charts has received"
    cy.get(selector.emailDeliverability.complainsRateDomain)
      .its("length")
      .should("gt", 0)
  })
})
