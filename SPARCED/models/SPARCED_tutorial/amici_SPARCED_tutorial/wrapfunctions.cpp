#include "amici/model.h"
#include "wrapfunctions.h"
#include "SPARCED_tutorial.h"

namespace amici {
namespace generic_model {

std::unique_ptr<amici::Model> getModel() {
    return std::unique_ptr<amici::Model>(
        new amici::model_SPARCED_tutorial::Model_SPARCED_tutorial());
}


} // namespace generic_model

} // namespace amici
