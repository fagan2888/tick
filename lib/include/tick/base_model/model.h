//
// Created by Martin Bompaire on 22/10/15.
//

#ifndef LIB_INCLUDE_TICK_BASE_MODEL_MODEL_H_
#define LIB_INCLUDE_TICK_BASE_MODEL_MODEL_H_

// License: BSD 3 clause

#include "tick/base/base.h"

#include <cereal/cereal.hpp>

#include <iostream>

// TODO: Model "data" : ModeLabelsFeatures, Model,Model pour les Hawkes
template <class T>
class TModel {
 public:
  TModel() {}
  virtual ~TModel() {}

  virtual const char *get_class_name() const { return "TModel<T>"; }

  virtual T loss_i(const ulong i, const Array<T> &coeffs) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual void grad_i(const ulong i, const Array<T> &coeffs, Array<T> &out) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual void grad(const Array<T> &coeffs, Array<T> &out) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual T loss(const Array<T> &coeffs) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual ulong get_epoch_size() const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual ulong get_n_samples() const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual ulong get_n_features() const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  // Number of parameters to be estimated. Can differ from the number of
  // features, e.g. when including an intercept.
  virtual ulong get_n_coeffs() const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual T sdca_dual_min_i(const ulong i, const T dual_i,
                            const Array<T> &primal_vector,
                            const T previous_delta_dual_i, T l_l2sq) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  /**
   * For SDCA, sometimes observations might be discarded (Poisson regression).
   * In this case this returns a mapping from the sampled observation (in [0,
   * rand_max)) to the observation position (in [0, n_samples)). If nullptr is
   * returned, then it means no index_map is required as the mapping is the
   * canonical inedx_map[i] = i
   */
  virtual SArrayULongPtr get_sdca_index_map() { return nullptr; }

  virtual BaseArray<T> get_features(const ulong i) const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual void sdca_primal_dual_relation(const T l_l2sq,
                                         const Array<T> &dual_vector,
                                         Array<T> &out_primal_vector) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual bool is_sparse() const { return false; }

  virtual bool use_intercept() const {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
    return false;
  }

  virtual T grad_i_factor(const ulong i, const Array<T> &coeffs) {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  virtual void compute_lip_consts() {
    TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name());
  }

  /**
   * @brief Get the maximum of all Lipschits constants
   * @note This will cache the obtained value for later calls
   */
  virtual T get_lip_max() { TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name()); }

  /**
   * @brief Get the mean of all Lipschits constants
   * @note This will cache the obtained value for later calls
   */
  virtual T get_lip_mean() { TICK_CLASS_DOES_NOT_IMPLEMENT(get_class_name()); }
};

using Model = TModel<double>;
using ModelPtr = std::shared_ptr<Model>;

#endif  // LIB_INCLUDE_TICK_BASE_MODEL_MODEL_H_