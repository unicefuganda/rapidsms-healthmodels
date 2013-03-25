Feature: Updating facility

 Scenario: Changes to HealthFacility should be logged
    Given I am logged in as admin
    And I create a new health facility
    When I edit a HealthFacility
    And I attempt to save
    Then I should see my facility changes are made
    And I should see my changes are logged
    And I see my changes in fred provider

 Scenario: Unsuccessful Changes to HealthFacility should create failure
   Given I am logged in as admin
   And I create a new health facility
   When I edit a Facility with invalid values
   And I attempt to save
   Then I should see an error
   And I should have a failure object created to report it

 Scenario: Create HealthFacility - Happy path
   Given I am logged in as admin
   And I create a new health facility
   Then I should see my facility in fred provider

 Scenario: Making a facility inactive
  Given I am logged in as admin
  And I create a new health facility
  When I mark the facility inactive
  And I attempt to save
  Then I should see my facility changed in fred provider

 Scenario: Store JSON - create
  When I create a facility
  Then I should see it is logged in reversion