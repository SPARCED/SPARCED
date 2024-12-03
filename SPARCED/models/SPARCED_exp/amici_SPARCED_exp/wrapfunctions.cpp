#include "amici/model.h"
#include "wrapfunctions.h"
#include "SPARCED_exp.h"

namespace amici {
namespace generic_model {

std::unique_ptr<amici::Model> getModel() {
    return std::unique_ptr<amici::Model>(
        new amici::model_SPARCED_exp::Model_SPARCED_exp());
}


} // namespace generic_model

} // namespace amici
