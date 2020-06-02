Feature: Labeling uploaded Images with it's features

  Scenario Outline: The user requests a catalog to detect the given objects and it's features in the image
    Given the user has selected a list of <images>
    And the user selected a list of detection <objects>
    And the user may select an <colors> filter
    When the user creates the object detection filter request
    Then the system should have created catalog
    And the system creates a <number> of catalog events for each image containing the given filters
    And the system creates a children object for the given color
    Examples: Object Filters
    | images                | objects     | colors    | number |
    | car.jpg               | car         | red, blue |   1    |
    | car.jpg, onix_red.jpg | car, bike   | ,         |   2    |
    | stop_sign.jpg         | stop_sign   | red       |   1    |

  Scenario Outline: The user requests a catalog to filter images with the given scenes
    Given the user has selected a list of <images>
    And the user selected the <scenes>
    When the user creates the scene filter request
    Then the system should have created catalog
    And the system creates a <number> of catalog events for each image containing the given filters
    Examples: Scene Filters
    | images                        | scenes      | number |
    | beach.jpg                     | beach       |   1    |
    | mountain.jpg, mountain_2.jpg  | mountain    |   2    |
    | city.jpg                      | city        |   1    |

  Scenario Outline: The user requests a catalog to filter images with the given objects
    Given the user has selected a list of <images>
    And the user selected a list of recognition <objects>
    When the user creates the object recognition filter request
    Then the system should have created catalog
    And the system creates a <number> of catalog events for each image containing the given filters
    Examples: Object Recognition Filters
    | images                        | objects     | number |
    | car.jpg                       | car         |   1    |
    | car.jpg, onix_red.jpg         | car         |   2    |