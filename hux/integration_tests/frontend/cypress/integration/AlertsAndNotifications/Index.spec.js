import route from "../../support/routes"
import selector from "../../support/selectors"

describe("Notifications", () => {
  beforeEach(() => {
    cy.signin()
    cy.visit(route.home)
  })

  it("should be able to view a list of notifications", () => {
    cy.location("pathname").should("eq", route.home)

    //notification bell icon should be visible
    cy.get(selector.notification.notificationicon).should("be.visible")
    //click on the bell button
    cy.get(selector.notification.notificationicon).click()
    // open open notification drop down and check the length of the data
    cy.get(selector.notification.notificationlistmenu).should(($menulist) => {
      expect($menulist).to.have.length(5)
    })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    // view all link should be visible
    cy.get(selector.notification.viewAllNotifications).should("be.visible")
    // click on the view all link
    cy.get(selector.notification.viewAllNotifications).click()
    // route in notification screen
    cy.location("pathname").should("eq", route.notifications)
    // scroll down for lazy loading
    cy.get(".table-overflow").scrollTo("bottom", { ensureScrollable: true })
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)

    cy.get(selector.notification.alertIdClick).eq(1).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.exitDrawer).click()
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.alertFilters).contains("Alert type").click()
    cy.get(selector.notification.alertFilters)
      .contains("Success")
      .click({ force: true })
    //clear all checkboxes and close the drawer
    // cy.get(selector.audience.audienceFilters).contains("Clear").click()
    cy.get(selector.notification.applyAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.clearAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.alertFilters).contains("Time(1)").click()
    cy.get(selector.notification.alertFilters)
      .contains("Today")
      .click({ force: true })
    cy.get(selector.notification.applyAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.alertFilters).contains("Time(1)").click()
    cy.get(selector.notification.alertFilters)
      .contains("All time")
      .click({ force: true })
    cy.get(selector.notification.applyAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.alertFilters).contains("Time(1)").click()
    cy.get(selector.notification.alertFilters)
      .contains("Last month")
      .click({ force: true })
    cy.get(selector.notification.applyAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertFilterToggle).click()
    cy.get(selector.notification.clearAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(2000)
    cy.get(selector.notification.closeAlertFilter).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertConfigureToggle).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureMainSwitch).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertConfigureSave).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureToggle).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureMainSwitch).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertConfigureSave).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureToggle).click()
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.individualSwitch).eq(1).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(500)
    cy.get(selector.notification.alertConfigureSave).click()
        // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureToggle).click()

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000)
    cy.get(selector.notification.alertConfigureCancel).click()
    // cy.get(selector.notification.exitDrawer).click()
    // click on the return to previous page button
    cy.get(selector.notification.notificationReturnButton).click()
  })
})
