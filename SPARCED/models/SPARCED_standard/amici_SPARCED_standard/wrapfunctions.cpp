#include "amici/model.h"
#include "wrapfunctions.h"
#include "SPARCED_I.h"

namespace amici {
namespace generic_model {

std::unique_ptr<amici::Model> getModel() {
    return std::unique_ptr<amici::Model>(
        new amici::model_SPARCED_I::Model_SPARCED_I());
}


} // namespace generic_model

} // namespace amici
