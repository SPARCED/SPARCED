#include "amici/model.h"
#include "wrapfunctions.h"
#include "SPARCED_standard.h"

namespace amici {
namespace generic_model {

std::unique_ptr<amici::Model> getModel() {
    return std::unique_ptr<amici::Model>(
        new amici::model_SPARCED_standard::Model_SPARCED_standard());
}


} // namespace generic_model

} // namespace amici
